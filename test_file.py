from pymodm import connect
from pymodm import MongoModel, fields


class Patient(MongoModel):
    patient_id = fields.CharField(primary_key=True)
    attending_email = fields.CharField()
    user_age = fields.CharField()
    heart_rate = fields.CharField()
    heart_rate_average_since = fields.CharField()


r = {'patient_id': 1, 'attending_email': 'dn56@duke.edu', 'user_age': 22}
new_patient = Patient(r['patient_id'], attending_email=r['attending_email'], user_age=r['user_age'])
print(new_patient)
