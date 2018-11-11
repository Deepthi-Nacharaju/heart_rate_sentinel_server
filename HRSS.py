from flask import Flask, jsonify, request
import math
import requests
app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    r = request.get_json()
    return jsonify(r)


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    r = request.get_json()
    return jsonify(r)


@app.route("/api/status/patient", methods=["GET"])
def is_patient():
    # do things
    return


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_patient():
    # do things

    return


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def avg_patient():
    # do things

    return


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def heart_rate():
    r = request.get_json()
    return jsonify(r)


if __name__ == "__main__":
    app.run(host="127.0.0.1")
