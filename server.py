from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def start():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/learn/<int:lesson_number>")
def learn(lesson_number):
    return render_template("learn.html", lesson_number=lesson_number)

@app.route("/quiz/<int:question_number>")
def quiz(question_number):
    return render_template("quiz.html", question_number=question_number)

@app.route("/results")
def results():
    return render_template("results.html")

if __name__ == "__main__":
    app.run(debug=True)

