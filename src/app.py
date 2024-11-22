'''
Main Code for creating the Web Interface
'''

###IMPORTS###

#Flask Imports
from flask import Flask, render_template, request, make_response, redirect, url_for
from flask_socketio import SocketIO
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

#Google imports
from oauthlib.oauth2 import WebApplicationClient
from google.oauth2 import id_token
from google.auth.transport import requests

#SQL

import os
import json

from db import init_db_command, db_error
from User import User
from Sockets import *
#import Game

from random_username.generate import generate_username



app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
socketio = SocketIO(app, cors_allowed_origins="*")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
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
@login_required
def admin():
    if current_user.is_admin():
        return render_template("admin.html")
    return redirect("/login")


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/login")
def login():
    return render_template("login.html", client=GOOGLE_CLIENT_ID)

'''
@app.route("/login/google")
def google():
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

@app.route("/login/local",methods=["POST"])
def callback():
    token = request.form.get("auth_token")

    user = User.get(unique_id)

    if not user:
        User.create(unique_id, users_name, users_email, picture)
        user = User.get(unique_id)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect("/play")'''
    

@app.route("/login/callback",methods=["POST"])
def callback():
    '''csrf_token_cookie = request.cookies.get('g_csrf_token')
    if not csrf_token_cookie:
        webapp2.abort(400, 'No CSRF token in Cookie.')
    csrf_token_body = request.get('g_csrf_token')
    if not csrf_token_body:
        webapp2.abort(400, 'No CSRF token in post body.')
    if csrf_token_cookie != csrf_token_body:
        webapp2.abort(400, 'Failed to verify double submit cookie.')
    '''

    token = request.form.get("credential")

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        unique_id = idinfo['sub']
        users_email = idinfo["email"]
        picture = idinfo["picture"]
        users_name = idinfo["given_name"]

        user = User.get(unique_id)

        if not user:
            User.create(unique_id, users_name, users_email, picture)
            user = User.get(unique_id)

        # Begin user session by logging the user in
        login_user(user)

        # Send user back to homepage
        return redirect("/play")
    
    except ValueError:
        # Invalid token
        return "User email not available or not verified by Google.", 400
    

@app.route("/play",methods=["GET"])
def play():
    if not current_user.is_authenticated:
        #TODO: add guest functionality
        usr = generate_username()[0]
        User.create(usr,usr,f"{usr}@GUEST","/static/res/def_profile.png")
        login_user(User.get(usr))

    return render_template("game.html", name = current_user.name,email= current_user.email,img= current_user.profile_pic,balance=current_user.balance)
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

#socketio.on_namespace(Home("/"))
socketio.on_namespace(Playing('/play'))
socketio.on_namespace(Admin("/admin"))

if __name__ == '__main__':
    try:
        init_db_command()
        #print ()
    except db_error as e:
        # Assume it's already been created
        print(e)
        pass

    socketio.run(app,host="0.0.0.0",ssl_context='adhoc')