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
    ('Word', 'Word', 1),

])
def test_is_tachy(age, rate, expected):
    result = is_tachy(age, rate)
    assert result == expected
