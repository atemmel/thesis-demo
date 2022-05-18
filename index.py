#!/usr/bin/env python

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from threading import Lock
import load

obj = load.load_model_data()
obj_mutex = Lock()

app = Flask(__name__)
CORS(app)

def dumpS(what):
    with open(what) as file:
        return file.read();


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

@app.route("/", methods=["GET"])
def index():
    return dumpS("www/index.html")

@app.route("/script.js", methods=["GET"])
def script():
    return dumpS("www/script.js")

@app.route("/style.css", methods=["GET"])
def style():
    return dumpS("www/style.css")

if __name__ == '__main__':
    app.run()
