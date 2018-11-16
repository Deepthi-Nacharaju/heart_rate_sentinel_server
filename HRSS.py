from flask import Flask, jsonify, request
import math
import requests
import pymodm
from pymodm import connect
from pymodm import MongoModel, fields
import datetime
import sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from dateutil import parser

app = Flask(__name__)
connect("mongodb://dnacharaju:goduke10@ds059365.mlab.com:59365/bme590")  # connect to database


class Patient(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.CharField()
    user_age = fields.IntegerField()
    heart_rate = fields.ListField()
    heart_rate_time = fields.ListField()


@app.route("/api/new_patient", methods=["POST"])
def post_new_patient():
    """
    POSTS new patient with patient_id, attending_email, and user_age
    Returns: posted dictionary

    """
    r = request.get_json()
    patient = Patient(int(r['patient_id']), attending_email=r['attending_email'], user_age=int(r['user_age']))
    patient.save()
    print(patient.patient_id)
    return jsonify(r)


@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    """
    POSTS heart_rate for patient_id
    Returns: posted dictionary

    """
    r = request.get_json()
    patient = Patient.objects.raw({'_id': int(r['patient_id'])}).first()
    try:
        patient.heart_rate.append(r['heart_rate'])
        patient.heart_rate_time.append(datetime.datetime.now().isoformat())
        patient.save()
    except AttributeError:
        patient.heart_rate = int(r['heart_rate'])
        patient.heart_rate_time = datetime.datetime.now().isoformat()
        patient.save()
    out = is_tachy(patient.user_age, int(r['heart_rate']))
    if out:
        send_email(patient.attending_email, patient.patient_id, patient.heart_rate)
    r['heart_rate'] = patient.heart_rate
    return jsonify(r)


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_is_patient(patient_id):
    """
    GET request that returns if patient is tachycardic based on last posted heart rate
    Args:
        patient_id: usually patient mrn

    Returns: If patient is tachycardic, and heart rate

    """
    for patient in Patient.objects.raw({"patient_id": format(patient_id)}):
        rate = patient.heart_rate[-1]
        age = patient.user_age
        out = is_tachy(age, rate)
    if out:
        return jsonify(('Tachycardic', rate))
    else:
        return jsonify('Not tachycardic')


def is_tachy(age, rate):
    """

    Args:
        age: age of patient
        rate: heart rate of patient

    Returns: 1 if tachycardic, 0 if not

    """
    age = float(age)
    rate = int(rate)
    if float(1 / 7 / 4 / 12) <= age <= float(2 / 7 / 4 / 12) and rate > 159:
        out = 1
    elif float(3 / 7 / 4 / 12) <= age <= float(6 / 7 / 4 / 12) and rate > 166:
        out = 1
    elif float(1 / 4 / 12) <= age <= float(3 / 4 / 12) and rate > 182:
        out = 1
    elif 1 / 12 <= age <= 2 / 12 and rate > 179:
        out = 1
    elif 3 / 12 <= age <= 5 / 12 and rate > 186:
        out = 1
    elif 6 / 12 <= age <= 11 / 12 and rate > 169:
        out = 1
    elif 1 <= age <= 2 and rate > 151:
        out = 1
    elif 3 <= age <= 4 and rate > 137:
        out = 1
    elif 5 <= age <= 7 and rate > 133:
        out = 1
    elif 8 <= age <= 11 and rate > 130:
        out = 1
    elif 12 <= age <= 15 and rate > 119:
        out = 1
    elif age > 15 and rate > 100:
        out = 1
    else:
        out = 0
    return out


def send_email(receiver, patient_id, heart_rate):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("heart_rate_server@duke.edu")
    to_email = Email(receiver)
    subject = 'Urgent! Patient ' + str(patient_id) + ' is Tachycardic!'
    content = Content("text/plain", "Patient " + str(patient_id) + " is Tachycardic with a heart rate of "
                      + str(heart_rate))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    return


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_patient(patient_id):
    patient = Patient.objects.raw({'_id': int(patient_id)}).first()
    hr = patient.heart_rate
    return jsonify(hr)


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_avg_patient(patient_id):
    patient = Patient.objects.raw({'_id': int(patient_id)}).first()
    hr = patient.heart_rate
    avg = float(sum(hr)) / float(len(hr))
    return jsonify(avg)


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_heart_rate_avg():
    r = request.get_json()
    patient = Patient.objects.raw({'_id': r['patient_id']}).first()
    print(patient)
    sum_hr = 0
    count = 0
    time_array = patient.heart_rate_time
    print(type(patient.heart_rate))
    dt_thresh = parser.parse(r['heart_rate_average_since'])
    for index, time in enumerate(time_array):
        dt_object = parser.parse(time)
        if dt_object > dt_thresh:
            sum_hr += patient.heart_rate[index]
            count += 1
    avg = float(sum_hr) / float(count)
    return jsonify(avg)


@app.route("/name", methods=["GET"])
def name():
  """
  Returns the string "Hello, world" to the caller
  """
  return_dict = {"name": "Deepthi Nacharaju"}
  return jsonify(return_dict)



if __name__ == "__main__":
    connect("mongodb://dnacharaju:goduke10@ds059365.mlab.com:59365/bme590")  # connect to database
    #app.run(host="127.0.0.1")
    app.run(host="0.0.0.0")
