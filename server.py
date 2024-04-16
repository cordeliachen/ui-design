from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)

# Load your dataset
with open("dataset.json") as f:
    data = json.load(f)


@app.route("/")
def start():
    return render_template("home.html")


@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/learn/<int:lesson_id>')
def learn(lesson_id):
    with open('static/data/lessons.json') as f:
        lessons = json.load(f)
    lesson = lessons.get(str(lesson_id))
    max_lesson_id = len(lessons)  # Adapting for dynamic lesson IDs
    return render_template('learn.html', lesson=lesson, max_lesson_id=max_lesson_id)




if __name__ == "__main__":
    app.run(debug=True)
