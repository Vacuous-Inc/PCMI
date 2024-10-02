'''
Main Code for creating the Web Interface
'''

from flask import Flask, render_template, request, make_response
import Game
import Camera
import Physical
import DatabaseConnection as db

app = Flask(__name__)

data = db.db();

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/spectate", methods=["GET"])
def watch():
    return render_template("watch.html")

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin_login.html")

@app.route("/join",methods=["GET"])
def join():
    return render_template("join.html")

@app.route("/play",methods=["GET"])
def play():
    return render_template("game.html")