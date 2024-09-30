from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/spectate", methods=["GET"])
def watch():
    return render_template("watch.html")

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin_login.html")

@app.route("/play",methods=["GET"])
def play():
    return render_template("game.html")