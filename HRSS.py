from flask import Flask, jsonify, request
import math
import requests
app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def post_new_patient():
    r = request.get_json()
    return jsonify(r)


@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    r = request.get_json()
    return jsonify(r)


@app.route("/api/status/patient", methods=["GET"])
def get_is_patient():
    # do things
    r = request.get_json()
    return print(jsonify(r))


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_patient():
    # do things

    return


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_avg_patient():
    # do things

    return


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_heart_rate_avg():
    r = request.get_json()
    return jsonify(r)


if __name__ == "__main__":
    app.run(host="127.0.0.1")
