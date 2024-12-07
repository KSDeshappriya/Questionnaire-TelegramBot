from pyrogram import Client, filters
from google_drive import create_folder, upload_file, share_folder
from firebase_utils import get_questions, save_response, has_submitted, db
import os
import uuid
import datetime

# creator
creator_fiverr = "https://www.fiverr.com/ksdeshp"
creator_linkdin = "https://www.linkedin.com/in/kavindu-shehan-917031255/"
creator_email = "ksdeshappriya.official@gmail.com"

# Initialize the Telegram bot client
app = Client(f"{os.getenv("BOT_USERNAME")}", bot_token=os.getenv("BOT_TOKEN"), api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"))

user_data = {}  # Temporary storage for user sessions

# Start command, initialize user data
@app.on_message(filters.command("start"))
async def start(client, message):
    # if has_submitted(str(message.from_user.id)):
    #     await message.reply("<i>Welcome back!</i> <b>You have already submitted your response!</b>")
    #     return

    # Initialize user session with both answers and images keys
    user_data[message.from_user.id] = {"answers": {}, "images": [], "current_q": 0}
    # Send a welcome message
    welcome_message = (
        f"<b>Hello @{message.from_user.first_name} !</b>\n\n"
        "<b>Welcome to our survey bot.</b> We'll ask you a few questions, and you can "
        "respond with text or images as requested. Let's get started!"
        f"\n\n<i>Created by <b>ksdeshp</b></i>: [onFiverr]({creator_fiverr}) | [onLinkedIn]({creator_linkdin}) |"
    )
    await message.reply(welcome_message)
    await ask_next_question(message)

# Function to ask the next question
async def ask_next_question(message):
    user_id = message.from_user.id
    questions = get_questions()  # Fetch the list of questions
    current_q = user_data[user_id]["current_q"]

    # Check if there are still questions left to ask
    if current_q < len(questions):
        question = questions[current_q]
        print(f"Current Question: {current_q + 1} of {len(questions)}")

        if "type" in question and question["type"] == "text":
            await message.reply(f"<b>Question {current_q + 1}:</b> {question['text']}")
        elif "type" in question and question["type"] == "image":
            await message.reply(f"<b>Question {current_q + 1}:</b> {question['text']}")
        else:
            await message.reply(f"<b>Question {current_q + 1}:</b> {question['text']}")  # Fallback to text if type is missing or invalid
    else:
        await complete_form(message)  # If no more questions, complete the form

# Handle text responses
@app.on_message(filters.text & ~filters.command("start"))
async def handle_text_response(client, message):
    user_id = message.from_user.id
    current_q = user_data[user_id]["current_q"]
    questions = get_questions()

    if current_q < len(questions):
        question_id = questions[current_q]["question_id"]
        user_data[user_id]["answers"][question_id] = message.text
        print(f"Updated answers for user {user_id}: {user_data[user_id]['answers']}")  # Print answers for debugging
        user_data[user_id]["current_q"] += 1  # Move to the next question
        await ask_next_question(message)  # Ask the next question

# Handle image uploads
@app.on_message(filters.photo)
async def handle_image(client, message):
    user_id = message.from_user.id

    file_path = await message.download()  # Download the image to the local file system
    user_data[user_id]["images"].append(file_path)  # Store the image path

    # After image is uploaded, move to the next question
    user_data[user_id]["current_q"] += 1
    await ask_next_question(message)  # Ask the next question

# Function to complete the form after all questions are answered
async def complete_form(message):
    user_id = message.from_user.id  # Ensure user_id is a string

    # Initialize user data if not present
    if user_id not in user_data:
        print(f"New user: {user_id}, initializing data.")
    else:
        print(f"User {user_id} already exists, accessing data.")

    answers = user_data[user_id]["answers"]
    answers["1"] = answers.get("1", "Uncategorized").lower()
    images = user_data[user_id]["images"]

    print(answers)
    await message.reply("<b>This is the end of the questions.</b> <i>Wait for the responses to be saved.</i>")

    # Assume that the first answer determines the category (e.g., "Bat", "Ball", "Car")
    category = answers.get("1", "Uncategorized").lower()  # Fallback to "Uncategorized" if answer is missing
    parent_folder = create_folder(category)  # Create a parent folder in Google Drive
    unique_id = f"{user_id}-{uuid.uuid4().hex[:6]}"  # Generate a unique ID for this submission
    subfolder = create_folder(unique_id, parent_folder)  # Create a subfolder for this specific entry

    # Save answers to a text file
    answers_file = f"{unique_id}.txt"
    with open(answers_file, "w") as f:
        for q, a in answers.items():
            f.write(f"{q}: {a}\n")
    upload_file(answers_file, subfolder)  # Upload the answers file to Google Drive
    os.remove(answers_file)  # Clean up the local file

    # Upload images to the subfolder in Google Drive
    # Save images and collect file IDs
    image_file_ids = []
    downloads_dir = "./downloads"
    os.makedirs(downloads_dir, exist_ok=True) # Create downloads directory if it doesn't exist

    for image in images:
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = os.path.basename(image)
            new_file_name = os.path.join(downloads_dir, f"{category}-{timestamp}-{file_name}")
            os.rename(image, new_file_name)
            file_id = upload_file(new_file_name, subfolder) # Use the new file name
            if file_id:
                image_file_ids.append(file_id)
                os.remove(new_file_name) #remove after upload

        except FileNotFoundError as e:
            print(f"Error: File not found - {e}")
            #Consider adding logging here for more robust error handling.
        except OSError as e:
            print(f"Error during file operation: {e}")
            #Consider adding logging here for more robust error handling.
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            #Consider adding logging here for more robust error handling.

    # Save the response details (this could be a call to Firebase or another storage system)
    save_response(user_id, unique_id, share_folder(parent_folder), share_folder(subfolder), answers, image_file_ids)

    # Send confirmation to the user
    await message.reply(f"<b>Your response has been saved!</b> <i>ID: {unique_id}</i>")

    # Cleanup the user session
    del user_data[user_id]

# Run the bot
app.run()
