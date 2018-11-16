import pytest
from HRSS import is_tachy
import requests


@pytest.mark.parametrize('age, rate, expected', [
    (1 / 7 / 4 / 12, 170, 1),
    (1 / 7 / 4 / 12, 100, 0),
    (4/7/4/12, 170, 1),
    (4 / 7 / 4 / 12, 100, 0),
    (2/4/12, 200, 1),
    (2 / 4 / 12, 100, 0),
    (float(1.5/12), 200, 1),
    (float(1.5/12), 100, 0),
    (.33, 190, 1),
    (.33, 170, 0),
    (.5, 170, 1),
    (.5, 139, 0),
    (1, 200, 1),
    (1, 100, 0),
    (3, 200, 1),
    (3, 100, 0),
    (6, 140, 1),
    (6, 100, 0),
    (9, 200, 1),
    (9, 70, 0),
    (13, 70, 0),
    (13, 200, 1),
    (18, 200, 1),
    (18, 86, 0),

])
def test_is_tachy(age, rate, expected):
    result = is_tachy(age, rate)
    assert result == expected


@pytest.mark.parametrize("server, dictionary, expected", [
    ("http://127.0.0.1:5000/api/new_patient",
     {"patient_id": 1, "attending_email": 'dn56@duke.edu', "user_age": 22},
     {"patient_id": 1, "attending_email": 'dn56@duke.edu', "user_age": 22}),
    ("http://127.0.0.1:5000/api/new_patient",
     {"patient_id": '1', "attending_email": 'dn56@duke.edu', "user_age": '22'},
     {"patient_id": 1, "attending_email": 'dn56@duke.edu', "user_age": 22}),
])
def test_post_new_patient(server, dictionary, expected):
    r = requests.post(server, json=dictionary)
    assert expected == r.json()
