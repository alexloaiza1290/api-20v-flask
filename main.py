from flask import render_template, request, redirect, url_for, flash, jsonify
from api_20v_flask import create_app
from api_20v_flask.models import post

app = create_app()
app.secret_key = "eJ0Af987ADBdeaTseXZf58fcMydskHRK"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", name_page="blog")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html", name_page="about")


@app.route("/posts", methods=["GET"])
def get_all_post():
    posts_list = post.get_all_posts()

    if request.args.get("format") == "json":
        return jsonify([dict(p) for p in posts_list])

    return render_template("post/post_list.html", posts_list=posts_list)


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_one_post(post_id):
    p = post.get_post_by_id(post_id)
    if not p:
        flash("El post solicitado no existe.", "danger")
        return redirect(url_for("get_all_post"))

    if request.args.get("format") == "json":
        return jsonify(dict(p))

    return render_template('post/post.html', post=p)


@app.route("/posts/create", methods=["GET", "POST"])
def create_one_post():
    if request.method == "GET":
        return render_template("post/create.html")

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        flash("Título y contenido son obligatorios.", "warning")
        return redirect(url_for("create_one_post"))

    post.create_post(title, content)
    flash("Post creado exitosamente", "success")
    return redirect(url_for('get_all_post'))


@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_one_post(post_id):
    p = post.get_post_by_id(post_id)
    if not p:
        flash("El post solicitado no existe.", "danger")
        return redirect(url_for("get_all_post"))

    if request.method == "GET":
        return render_template('post/update.html', post=p)

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        flash("Título y contenido no pueden estar vacíos.", "warning")
        return redirect(url_for("edit_one_post", post_id=post_id))

    post.update_post(post_id, title, content)
    flash("Post actualizado correctamente", "success")
    return redirect(url_for('get_all_post'))


@app.route('/posts/delete/<int:post_id>', methods=['POST'])
def delete_one_post(post_id):
    p = post.get_post_by_id(post_id)
    if not p:
        flash("El post que intentas eliminar no existe.", "danger")
        return redirect(url_for("get_all_post"))

    post.delete_post(post_id)
    flash("Post eliminado", "info")
    return redirect(url_for('get_all_post'))


if __name__ == '__main__':
    app.run(debug=True)
