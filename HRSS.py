from flask import Flask, jsonify, request
import math
import requests
import pymodm
from pymodm import connect
from pymodm import MongoModel, fields
app = Flask(__name__)
connect("mongodb://<dnacharaju>:<goduke10>@ds059365.mlab.com:59365/bme590")  # connect to database


class Patient(MongoModel):
    patient_id = fields.CharField(primary_key=True)
    attending_email = fields.CharField()
    user_age = fields.CharField()
    heart_rate = []
    heart_rate_time =[]
    heart_rate_average_since = fields.CharField()

@app.route("/api/new_patient", methods=["POST"])
def post_new_patient():
    r = request.get_json()
    new_patient = Patient(r['patient_id'], attending_email=r['attending_email'], user_age=r['user_age'])
    new_patient.save()
    return print(new_patient)


@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    r = request.get_json()
    for patient in Patient.objects.raw({"patient_id": r['patient_id']}):
        patient.heart_rate.append(r['heart_rate'])
        patient.heart_Rate_time.append(r['timestamp'])
    return


@app.route("/api/status/,<patient_id>", methods=["GET"])
def get_is_patient(patient_id):
    for patient in Patient.objects.raw({"patient_id": format(patient_id)}):
        rate = patient.heart_rate[-1]
        age = patient.user_age
        if float(1/7/4/12) <= age <= float(2/7/4/12) and rate >159:
            out = ('Tachychardic', patient.heart_rate_time[-1])
        elif float(3/7/4/12) <= age <= float(6/7/4/12) and rate >166:
            out = ('Tachychardic', patient.heart_rate_time[-1])
        elif float(1/4/12) <= age <= float(3/4/12) and rate > 182:
            out = ('Tachychardic', patient.heart_rate_time[-1])
        elif 1/12 <= age <= 2/12 and rate > 179:
            out = ('Tachychardic', patient.heart_rate_time[-1])
        elif 3/12 <= age <= 5/12 and rate > 186:
            out = ('Tachychardic', patient.heart_rate_time[-1])
        elif 6/12 <= age <= 11/12 and rate > 169:
            out = ('Tachychardic', patient.heart_rate_time[-1])
        elif 1 <= age <= 2 and rate > 151:
            out = ('Tachychardic', patient.heart_rate_time[-1])
        elif 3 <= age <= 4 and rate > 137:
            out = ('Tachychardic', patient.heart_rate_time[-1])
        elif 5 <= age <= 7 and rate > 133:
            out = ('Tachychardic', patient.heart_rate_time[-1])
        elif 8 <= age <= 11 and rate > 130:
            out = ('Tachychardic', patient.heart_rate_time[-1])
        elif 12 <= age <= 15 and rate > 119:
            out = ('Tachychardic', patient.heart_rate_time[-1])
        elif age > 15 and rate > 100:
            out = ('Tachychardic', patient.heart_rate_time[-1])
    return print(out)


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_patient(patient_id):
    for patient in Patient.objects.raw({"patient_id": format(patient_id)}):
        rate = patient.heart_rate
    return rate


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_avg_patient(patient_id):
    for patient in Patient.objects.raw({"patient_id": format(patient_id)}):
        rate = patient.heart_rate
    avg = float(sum(rate)) / float(len(rate))
    return avg


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_heart_rate_avg():
    r = request.get_json()
    return jsonify(r)


if __name__ == "__main__":
    app.run(host="127.0.0.1")