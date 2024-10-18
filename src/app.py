'''
Main Code for creating the Web Interface
'''

from flask import Flask, render_template, request, make_response, redirect, url_for
from flask_socketio import SocketIO
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
import sqlite3

import os
import json

from db import init_db_command
from User import User
import Game
from Sockets import *
#import Camera
#import Physical
#import DatabaseConnection as db

from random_username.generate import generate_username

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

login_manager = LoginManager()
login_manager.init_app(app)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/spectate", methods=["GET"])
def watch():
    return render_template("watch.html")

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin_login.html")

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    user = User.get(unique_id)

    # Doesn't exist? Add it to the database.
    if not user:
        User.create(unique_id, users_name, users_email, picture)
        user = User.get(unique_id)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect("/play")

@app.route("/play",methods=["GET"])
def play():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        #TODO: add guest functionality
        #generate_username(5)
        return '<a class="button" href="/login">Google Login</a>'
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

#socketio.on_namespace(Home("/"))
#socketio.on_namespace(Playing('/play'))
#socketio.on_namespace(Admin("/admin"))

if __name__ == '__main__':
    try:
        init_db_command()
        #print ()
    except sqlite3.OperationalError as e:
        # Assume it's already been created
        print(e)
        pass

    socketio.run(app,ssl_context='adhoc')