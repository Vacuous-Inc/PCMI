'''
Code to control the camera
'''

from flask import Flask, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

@app.route("/data", methods = ["GET"])
def get_data():
    cards = []
    resp = {"Cards":cards}
    return jsonify(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0")