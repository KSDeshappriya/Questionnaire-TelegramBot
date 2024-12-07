import firebase_admin
from firebase_admin import credentials, firestore
import os
import uuid

# Initialize Firebase
cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS_PATH"))
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_questions():
    """Retrieve all questions from Firestore."""
    questions = db.collection("questions").order_by("question_id").get()
    return [q.to_dict() for q in questions]

def save_response(user_id, unique_id, parentFolder, subfolder, answers, images):
    # Ensure user_id is a string
    user_id = str(user_id)

    # db.collection("responses").document(user_id).set({
    #     "unique_id": unique_id,
    #     "parentFolder": parentFolder,
    #     "folder": subfolder,
    #     "answers": answers,
    #     "images": images
    # })

    # unique_id = f"{user_id}-{uuid.uuid4().hex[:6]}"
    db.collection("responses").document(unique_id).set({
        "unique_id": unique_id,
        "user_id": user_id,
        "parentFolder": parentFolder,
        "folder": subfolder,
        "answers": answers,
        "images": images,
        "timestamp": firestore.SERVER_TIMESTAMP,
    })


def has_submitted(user_id):
    """Check if a user has already submitted the form."""
    doc = db.collection("responses").document(user_id).get()
    return doc.exists
