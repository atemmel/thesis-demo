#!/usr/bin/env python

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from random import randint
from threading import Lock
import load

obj = load.load_model_data()
obj_mutex = Lock()

app = Flask(__name__)
CORS(app)

def do_prediction():
    return randint(0, 1)


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

if __name__ == '__main__':
    app.run()
