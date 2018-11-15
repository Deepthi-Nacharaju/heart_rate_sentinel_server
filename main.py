import requests
import logging
import datetime
import sendgrid
import os
import pymodm
from sendgrid.helpers.mail import *
from pymodm import connect
from pymodm import MongoModel, fields


class Patient(MongoModel):
    patient_id = fields.IntegerField(primary_key=True)
    attending_email = fields.CharField()
    user_age = fields.FloatField()
    heart_rate = fields.IntegerField()
    heart_rate_average_since = fields.IntegerField()


def post_new_patient(parameters, server=None):
    """

    Args:
        parameters: Array or list of patient id, attending email, and user age
        server: string of server requests are intended to run on

    Returns:
        json of dictionary that was posted
    """
    if not server:
        server = "http://127.0.0.1:5000/api/new_patient"
    else:
        server = server + '/api/new_patient'
    post_dictionary = {"patient_id": parameters[0],  # usually this would be the patient MRN
                       "attending_email": parameters[1],
                       "user_age": parameters[2],  # in years
                       }
    #try:
    r = requests.post(server, json=post_dictionary)
    #print(r.json())
    #except:
    #    logging.warning('New Patient Error: Check Inputs')
    return print(r.json())


def post_heart_rate(parameters, server=None):
    """

    Args:
        parameters: array or list with patient id and heart rate
        server: url address (optional arg: default set to local)

    Returns:
        json of what was posted
    """
    if not server:
        server = "http://127.0.0.1:5000/api/heart_rate"
    else:
        server = server + '/api/heart_rate'
    post_dictionary = {"patient_id": parameters[0],  # usually this would be the patient MRN
                       "heart_rate": parameters[1],
                       "timestamp": str(datetime.datetime.now()),
                       }
    #try:
    r = requests.post(server, json=post_dictionary)
    #except:
    #    logging.warning('Heart Rate Error: Check Inputs')
    return print(r.json())


def get_heart_rates(parameters, server=None):
    if not server:
        server = "http://127.0.0.1:5000/api/heart_rate/{}".format(parameters[0])
    else:
        server = server + '/api/heart_rate{}'.format(parameters[0])
    r = requests.get(server)
    return


def send_email(receiver, patient_id):
    """

    Args:
        receiver: email string of recipient
        patient_id: often mrn number

    Returns:
        success of sending an email

    """
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("test@example.com")
    to_email = Email(receiver)  # string of email of recipient
    subject = "WARNING: Tachycardic Patient"
    content = Content("text/plain", "Patient " + str(patient_id) + " is tachycardic")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
    return


def post_avg_patient(parameters, server=None):
    """

    Args:
        parameters: array with patient id
        server: url address (optional arg: default set to local)

    Returns:
        printed string of post request
    """
    if not server:
        server = "http://127.0.0.1:5000/api/heart_rate"
    else:
        server = server + '/api/heart_rate'
    post_dictionary = {
        "patient_id": parameters[0],
        "heart_rate_average_since": parameters[1],  # date string
    }
    r = requests.post(server, post_dictionary)
    return


def main():
    server_url = "http://127.0.0.1:5000"  # must match app.run in HRSS.py
    #  os.system("FLASK_APP=flask_service.py flask run")
    post_new_patient((1, 'dn56@duke.edu', 40))
    post_heart_rate((1, 150))
    post_heart_rate((1, 100))
    get_heart_rates([1])
    # send_email('dn56@duke.edu', 1)
    return


if __name__ == "__main__":
    main()
