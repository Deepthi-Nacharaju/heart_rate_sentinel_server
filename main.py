import requests


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
    try:
        r = requests.post(server, json=post_dictionary)
    except:
        print('Check inputs')
    print(r.json())
    return


def main():

    return


if __name__ == "__main__":
    main()
