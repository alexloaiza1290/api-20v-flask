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

# @app.route("/home", methods=["GET"])
# def home():
#     name_page = "home"
#     return render_template("post/post_list.html", name_page=name_page)

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

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return render_template('post/post.html', post=post)

@app.route("/posts/create", methods=["GET", "POST"])
def create_one_post():
    if request.method == "GET":
        return render_template("post/create.html")
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_post'))

@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_one_post(post_id):
    if request.method == "GET":
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
        conn.close()
        return render_template('post/update.html', post=post)
    if request.method == "POST":
        conn = get_db_connection()
        title = request.form['title']
        content = request.form['content']
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_post'))

@app.route('/posts/delete/<int:post_id>', methods=['DELETE'])
def delete_one_post(post_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return ""

if __name__ == '__main__': 
    app.run(debug=True)