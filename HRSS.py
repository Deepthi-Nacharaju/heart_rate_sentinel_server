from flask import Flask, jsonify, request
import math
import requests
app = Flask(__name__)

@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    dictionary = {"patient_id": "1",  # usually this would be the patient MRN
    "attending_email": "suyash.kumar@duke.edu",
    "user_age": 50,  # in years
    }
  return