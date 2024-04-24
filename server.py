from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session  # Import Session from flask_session
import json

app = Flask(__name__)

# Secret key for signing the session

app.config['SECRET_KEY'] = 'your_secret_key_here'

# Session configuration
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

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
    return render_template("quiz.html", data=data.values())

@app.route("/quiz1")
def quiz1():
    return render_template("quiz1.html", data=data.values())


@app.route("/quiz2")
def quiz2():
    return render_template("quiz2.html", data=data.values())


@app.route("/quiz3")
def quiz3():  # Corrected function name
    return render_template("quiz3.html", data=data.values())


@app.route("/quiz4")
def quiz4():  # Corrected function name
    return render_template("quiz4.html", data=data.values())


import random


@app.route("/quiz5")
def quiz5():
    quiz_data = data.get("9", {})  # Safely get data for quiz 9
    steps = list(quiz_data.get("steps", {}).values())
    random.shuffle(steps)  # Shuffle the steps to scramble them on each page load
    return render_template("quiz5.html", steps=steps, data=data.values())


@app.route("/quiz6")
def quiz6():
    return render_template("quiz6.html", data=data.values())


@app.route("/submit_quiz/<int:quiz_id>", methods=["POST"])
def submit_quiz(quiz_id):
    correct_answers = {
        1: {"question1": "False", "question2": "The tools used"},
        2: {"question1": "True", "question2": "The type of yarn used"},
        3: {"question1": "True", "question2": "The tools used"},
        4: {"question1": "False", "question2": "The type of yarn used"},
    }
    total_quizzes = 4
    score = session.get("score", 0)
    quiz_answers = correct_answers.get(quiz_id, {})

    for key, correct_answer in quiz_answers.items():
        if request.form.get(key) == correct_answer:
            score += 1

    session["score"] = score

    # Redirect to the next quiz, or to the feedback page if it's the last quiz
    if quiz_id < total_quizzes:
        return redirect(url_for(f"quiz{quiz_id + 1}"))
    else:
        return redirect(url_for("feedback"))

    increment = request.get_json().get("increment", 0)
    score = session.get("score", 0)
    score += increment
    session["score"] = score


@app.route("/feedback")
def feedback():
    score = session.get("score", 0)  # Retrieve the final score from the session
    session.pop("score", None)  # Optionally reset the score
    return render_template("feedback.html", score=score)

if __name__ == "__main__":
    app.run(debug=True)

