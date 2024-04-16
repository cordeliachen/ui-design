from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load your dataset from the correct file
with open("dataset.json") as f:
    data = json.load(f)

@app.route("/")
def start():
    return render_template("home.html", data=data.values())

@app.route("/home")
def home():
    return render_template("home.html", data=data.values())

@app.route('/learn/<int:lesson_id>')
def learn(lesson_id):
    lesson = data.get(str(lesson_id))
    max_lesson_id = len(data)  # Adapting for dynamic lesson IDs
    return render_template('learn.html', lesson=lesson, max_lesson_id=max_lesson_id)
    
@app.route("/quiz")
def home():
    return render_template("home.html")

@app.route("/quiz_results")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)

