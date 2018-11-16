import requests
import logging
import datetime
from datetime import timedelta
import sendgrid
import os
import pymodm
from sendgrid.helpers.mail import *
from pymodm import connect
from pymodm import MongoModel, fields


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
    post_dictionary = {"patient_id": int(parameters[0]),  # usually this would be the patient MRN
                       "attending_email": parameters[1],
                       "user_age": parameters[2],  # in years
                       }
    r = requests.post(server, json=post_dictionary)
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
    post_dictionary = {"patient_id": int(parameters[0]),  # usually this would be the patient MRN
                       "heart_rate": parameters[1],
                       }
    print(post_dictionary)
    r = requests.post(server, json=post_dictionary)

    return print(r.json())


def get_heart_rates(parameters, server=None):
    if not server:
        server = "http://127.0.0.1:5000/api/heart_rate/{}".format(parameters[0])
    else:
        server = server + '/api/heart_rate/{}'.format(parameters[0])
    r = requests.get(server)
    print(r.json())
    return


def get_avg_heart_rate(parameters, server=None):
    if not server:
        server = "http://127.0.0.1:5000/api/heart_rate/average/{}".format(parameters[0])
    else:
        server = server + '/api/heart_rate/average/{}'.format(parameters[0])
    r = requests.get(server)
    print(int(r.json()))
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
        server = "http://127.0.0.1:5000/api/heart_rate/interval_average"
    else:
        server = server + '/api/heart_rate/interval_average'
    post_dictionary = {
        "patient_id": parameters[0],
        "heart_rate_average_since": parameters[1],  # date string
    }
    r = requests.post(server, json=post_dictionary)
    return print(r.json())


def main():
    server_url = 'http://vcm-7471.vm.duke.edu:5000'  # must match app.run in HRSS.py
    #server_url = None
    #  os.system("FLASK_APP=HRSS.py flask run")
    #post_new_patient(('2', 'dn56@duke.edu', 40), server_url)
    post_heart_rate((1, 650), server_url)
    #post_heart_rate((2, 150), server_url)
    # get_heart_rates([2], server_url)
    #get_avg_heart_rate([2], server_url)
    now = datetime.datetime.now() - timedelta(hours=1)
    now = now.isoformat()
    # post_heart_rate((1, 155))
    post_heart_rate((1, 900), server_url)
    post_heart_rate((1, 1000), server_url)
    # post_heart_rate((1, 900), server_url)
    post_avg_patient((1, now), server_url)
    return


if __name__ == "__main__":
    main()
