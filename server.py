from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session  # Import Session from flask_session
import json

app = Flask(__name__)

# Secret key for signing the session
app.config["SECRET_KEY"] = "your_secret_key_here"

# Session configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Initialize the session
Session(app)

# Load your dataset from the correct file
with open("dataset.json") as f:
    data = json.load(f)


@app.route("/")
def start():
    return render_template("home.html", data=data.values())


@app.route("/home")
def home():
    return render_template("home.html", data=data.values())


@app.route("/learn/<int:lesson_id>")
def learn(lesson_id):
    if lesson_id > 8:  # Check if the lesson ID is greater than 8
        return redirect(
            url_for("quiz1")
        )  # Redirect to the quiz page if lesson ID is greater than 8

    lesson = data.get(str(lesson_id))
    max_lesson_id = 8  # Set the maximum lesson ID to 8
    return render_template(
        "learn.html", lesson=lesson, max_lesson_id=max_lesson_id, data=data.values()
    )


@app.route("/quiz")
def quiz():
    return render_template("quiz1.html", data=data.values())


@app.route("/quiz1")
def quiz1():
    return render_template("quiz1.html", data=data.values())


@app.route("/quiz2")
def quiz2():
    return render_template(
        "quiz2.html", data=data.values(), steps=data.get("6")["steps"]
    )


@app.route("/quiz3")
def quiz3():  # Corrected function name
    return render_template(
        "quiz3.html", data=data.values(), steps=data.get("8")["steps"]
    )


@app.route("/quiz4")
def quiz4():
    quiz_data = data.get("4", {})  # Safely get data for quiz 4 with a default fallback
    return render_template("quiz4.html", quiz_data=quiz_data)



import random


@app.route("/quiz5")
def quiz5():
    quiz_data = data.get("9", {})  # Safely get data for quiz 9
    steps = list(quiz_data.get("steps", {}).values())
    random.shuffle(steps)  # Shuffle the steps to scramble them on each page load
    return render_template("quiz5.html", steps=steps, data=quiz_data)


@app.route("/quiz6")
def quiz6():
    return render_template("quiz6.html", data=data.values())


@app.route("/submit_quiz/<int:quiz_id>", methods=["POST"])
def submit_quiz(quiz_id):
    correct_answers = {
        1: {"question1": "False", "question2": "The tools used"},
        2: {"question1": "Single crochet"},
        3: {"question1": "Double crochet"},
        4: {"question1": "False", "question2": "The type of yarn used"},
        5: {"question2": "Slip Knot"}  # Added for quiz 5 second question
    }
    total_quizzes = 6  # Total number of quizzes now includes quiz 5
    score = session.get("score", 0)
    quiz_answers = correct_answers.get(quiz_id, {})

    correct = all(request.form.get(key) == quiz_answers[key] for key in quiz_answers)
    if correct:
        score += len(quiz_answers)  # Increment score by the number of correct answers
        session["score"] = score

    response = {
        "correct": correct,
        "next_url": url_for(f"quiz{quiz_id + 1}") if quiz_id < total_quizzes else url_for("feedback")
    }
    return json.dumps(response), 200 if correct else 400

@app.route("/submit_order_quiz/<int:quiz_id>", methods=["POST"])
def submit_order_quiz(quiz_id):
    # Correct order for Quiz 4
    correct_order_quiz4 = ['step3', 'step2', 'step4', 'step1']
    # Correct order for Quiz 5
    correct_order_quiz5 = ['step4', 'step2', 'step1', 'step3']

    # Select correct order based on quiz_id
    if quiz_id == 4:
        correct_order = correct_order_quiz4
    elif quiz_id == 5:
        correct_order = correct_order_quiz5
    else:
        correct_order = []

    # Fetch user order from request
    user_order = request.json.get('order', [])

    # Check if user order matches the correct order
    correct = user_order == correct_order
    if correct:
        # Update session score
        score = session.get("score", 0) + 1  # Increment score by 1 for correct arrangement
        session["score"] = score

    # Determine the next URL
    next_url = url_for("quiz5") if quiz_id == 4 else url_for("feedback") if quiz_id == 5 else url_for("home")

    # Return response
    return jsonify({
        "correct": correct,
        "next_url": next_url
    }), 200 if correct else 400



@app.route("/update_score_6", methods=["POST"])
def update_score_6():
    if request.json and request.json["correct"]:
        score = session.get("score", 0)
        score += 1
        session["score"] = score
    return "", 204


@app.route("/feedback")
def feedback():
    score = session.get("score", 0)  # Retrieve the final score from the session
    session.pop("score", None)  # Optionally reset the score
    return render_template("feedback.html", score=score)


if __name__ == "__main__":
    app.run(debug=True)
