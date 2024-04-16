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


@app.route("/learn/<id>")
def view(id):
    lesson = data.get(id)
    print(lesson)
    if lesson:
        return render_template("learn.html", lesson=lesson)


if __name__ == "__main__":
    app.run(debug=True)
