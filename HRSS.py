from flask import Flask, jsonify, request
import math
import requests
app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    r = requests.get_json()
    return jsonify(r)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():

    return jsonify(dictionary)

