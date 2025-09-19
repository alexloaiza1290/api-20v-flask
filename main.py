from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hola_mundo():
    return "<p>Hello, mundo!</p>"


@app.route("/home", methods=["GET"])
def home():
    numero_1 = "uno"
    return render_template("index.html", numero_1=numero_1)


if __name__ == '__main__': 
    app.run(debug=True)