from flask import Flask, render_template, request, redirect
from firebase_utils import db

app = Flask(__name__)

# --- Admin Panel Routes ---

@app.route("/")
def dashboard():
    """Display dashboard with questions and categories."""
    questions = db.collection("questions").order_by("question_id").get()
    responses = db.collection("responses").get()

    categories = {}
    for r in responses:
        category = r.to_dict()["answers"]["1"]  # First answer determines category
        categories[category] = categories.get(category, 0) + 1

    return render_template("dashboard.html", questions=[q.to_dict() for q in questions], categories=categories)

# --- Question Management ---

@app.route("/add_question", methods=["POST"])
def add_question():
    """Add a new question to Firestore."""
    question_text = request.form["text"]
    question_type = request.form["type"]

    question_docs = db.collection("questions").get()
    question_id = len(question_docs) + 1  # Assign next question ID

    db.collection("questions").document(str(question_id)).set({
        "question_id": str(question_id),
        "text": question_text,
        "type": question_type
    })
    return redirect("/")

@app.route("/delete_question/<question_id>", methods=["GET"])
def delete_question(question_id):
    """Delete a question from Firestore."""
    db.collection("questions").document(question_id).delete()
    return redirect("/")

@app.route("/edit_question/<question_id>", methods=["POST"])
def edit_question(question_id):
    """Edit an existing question."""
    question_text = request.form["text"]
    question_type = request.form["type"]

    db.collection("questions").document(question_id).update({
        "text": question_text,
        "type": question_type
    })
    return redirect("/")

# --- Response Management ---

@app.route("/responses/<category>")
def view_responses(category):
    """View responses filtered by category."""
    responses = db.collection("responses").get()
    filtered_responses = [
        r.to_dict() for r in responses if r.to_dict()["answers"]["1"] == category
    ]
    return render_template("responses.html", category=category, responses=filtered_responses)

if __name__ == "__main__":
    app.run(debug=True)
