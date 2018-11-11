from flask import Flask, jsonify, request
import math
import requests
app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    r = requests.get_json()
    return jsonify(dictionary)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    dictionary = {
        "patient_id": "1", # usually this would be the patient MRN
        "heart_rate": 100
    }
    return jsonify(dictionary)

