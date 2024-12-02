import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS_PATH"))
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_questions():
    """Retrieve all questions from Firestore."""
    questions = db.collection("questions").order_by("question_id").get()
    return [q.to_dict() for q in questions]

def save_response(user_id, unique_id, folder_path, answers, images):
    """Save user responses to Firestore."""
    db.collection("responses").document(user_id).set({
        "unique_id": unique_id,
        "folder": folder_path,
        "answers": answers,
        "images": images,
    })

def has_submitted(user_id):
    """Check if a user has already submitted the form."""
    doc = db.collection("responses").document(user_id).get()
    return doc.exists
