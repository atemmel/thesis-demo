#!/usr/bin/env python

from flask import Flask, request, jsonify, abort, send_from_directory
from flask_cors import CORS
from threading import Lock
import load

obj = load.load_model_data()
obj_mutex = Lock()

app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["POST"])
def predict():
    patient = request.json["patient"]

    response = jsonify({})
    
    obj_mutex.acquire()
    try:
        prediction = load.do_prediction(obj, patient)
        obj_mutex.release()
        response = jsonify(prediction)
    except:
        obj_mutex.release()
        abort(500)

    return response

@app.route("/<path:path>", methods=["GET"])
def get(path):
    return send_from_directory("www", path)

@app.route("/", methods=["GET"])
def index():
    return send_from_directory("www", "index.html")

"""
@app.route("/script.js", methods=["GET"])
def script():
    return dumpS("www/script.js")

@app.route("/style.css", methods=["GET"])
def style():
    return dumpS("www/style.css")
"""

if __name__ == '__main__':
    app.run()
