from flask import Flask, render_template
import sqlite3


def get_db_connection():
    connection = sqlite3.connect("database.db")
    return connection

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    name_page = "blog"
    return render_template("index.html", name_page=name_page)

@app.route("/home", methods=["GET"])
def home():
    name_page = "home"
    return render_template("home.html", name_page=name_page)

@app.route("/about", methods=["GET"])
def about():
    name_page = "about"
    return render_template("about.html", name_page=name_page)


if __name__ == '__main__': 
    app.run(debug=True)