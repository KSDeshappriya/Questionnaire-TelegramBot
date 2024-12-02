from pyrogram import Client, filters
from google_drive import create_folder, upload_file
from firebase_utils import get_questions, save_response, has_submitted
import os
import uuid

app = Client("bot", bot_token=os.getenv("BOT_TOKEN"))

user_data = {}  # Temporary storage for user sessions

@app.on_message(filters.command("start"))
async def start(client, message):
    if has_submitted(str(message.from_user.id)):
        await message.reply("You have already submitted your response!")
        return

    user_data[message.from_user.id] = {"answers": {}, "images": [], "current_q": 0}
    await ask_next_question(message)

async def ask_next_question(message):
    user_id = message.from_user.id
    questions = get_questions()
    current_q = user_data[user_id]["current_q"]

    if current_q < len(questions):
        question = questions[current_q]
        await message.reply(question["text"])
    else:
        await complete_form(message)

@app.on_message(filters.text & ~filters.command("start"))
async def handle_text_response(client, message):
    user_id = message.from_user.id
    current_q = user_data[user_id]["current_q"]
    questions = get_questions()

    if current_q < len(questions):
        user_data[user_id]["answers"][questions[current_q]["question_id"]] = message.text
        user_data[user_id]["current_q"] += 1
        await ask_next_question(message)

@app.on_message(filters.photo)
async def handle_image(client, message):
    user_id = message.from_user.id
    file_path = await message.download()
    user_data[user_id]["images"].append(file_path)
    await ask_next_question(message)

async def complete_form(message):
    user_id = str(message.from_user.id)
    answers = user_data[user_id]["answers"]
    images = user_data[user_id]["images"]

    category = answers["1"]  # Assuming the first question determines category
    parent_folder = create_folder(category)
    unique_id = f"{category}-{uuid.uuid4().hex[:6]}"
    subfolder = create_folder(unique_id, parent_folder)

    # Save answers
    answers_file = f"{unique_id}.txt"
    with open(answers_file, "w") as f:
        for q, a in answers.items():
            f.write(f"{q}: {a}\n")
    upload_file(answers_file, subfolder)
    os.remove(answers_file)

    # Save images
    for image in images:
        upload_file(image, subfolder)
        os.remove(image)

    save_response(user_id, unique_id, subfolder, answers, images)
    await message.reply(f"Your response has been saved! ID: {unique_id}")
    del user_data[user_id]

app.run()
