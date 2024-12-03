from pyrogram import Client, filters
from google_drive import create_folder, upload_file, share_folder
from firebase_utils import get_questions, save_response, has_submitted, db
import os
import uuid

# Initialize the Telegram bot client
app = Client("testingPyrogram_bot", bot_token=os.getenv("BOT_TOKEN"), api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"))

user_data = {}  # Temporary storage for user sessions

# Start command, initialize user data
@app.on_message(filters.command("start"))
async def start(client, message):
    if has_submitted(str(message.from_user.id)):
        await message.reply("<b>You have already submitted your response!</b>")
        return

    # Initialize user session with both answers and images keys
    user_data[message.from_user.id] = {"answers": {}, "images": [], "current_q": 0}
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
    images = user_data[user_id]["images"]

    print(answers)
    await message.reply("<b>This is the end of the questions.</b> <i>Wait for the responses to be saved.</i>")

    # Assume that the first answer determines the category (e.g., "Bat", "Ball", "Car")
    category = answers.get("1", "Uncategorized")  # Fallback to "Uncategorized" if answer is missing
    parent_folder = create_folder(category)  # Create a parent folder in Google Drive
    unique_id = f"{category}-{uuid.uuid4().hex[:6]}"  # Generate a unique ID for this submission
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
    for image in images:
        file_id = upload_file(image, subfolder)
        if file_id:
            image_file_ids.append(file_id)
        os.remove(image)

    # Save the response details (this could be a call to Firebase or another storage system)
    save_response(user_id, unique_id, share_folder(subfolder), answers, image_file_ids)

    # Send confirmation to the user
    await message.reply(f"<b>Your response has been saved!</b> <i>ID: {unique_id}</i>")

    # Cleanup the user session
    del user_data[user_id]

# Run the bot
app.run()
