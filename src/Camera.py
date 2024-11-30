'''
Code to control the camera
'''

from flask import Flask, jsonify
from CardRecognitionModel import yolo

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

@app.route("/data", methods = ["GET"])
def get_data():
    cards = yolo.get_cards() # todo process this
    resp = {"Cards":cards}
    return jsonify(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0")