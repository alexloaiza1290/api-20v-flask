from flask import Flask, render_template, request, redirect, url_for
import sqlite3

def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
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

@app.route("/posts", methods=["GET"])
def get_all_post():
    c = get_db_connection()
    posts = c.execute('SELECT * FROM posts').fetchall()
    c.close()
    return render_template("post/post_list.html", posts_list=posts)


@app.route("/posts/create", methods=["GET", "POST"])
def create_one():
    if request.method == "GET":
        return render_template("post/create.html")
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        print(title, content)
        return redirect(url_for('get_all_post'))
    

if __name__ == '__main__': 
    app.run(debug=True)