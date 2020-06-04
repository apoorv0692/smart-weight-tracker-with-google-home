import json
import logging
import app

failed_to_add_weight = {
    "payload": {
        "google": {
        "expectUserResponse": "true",
        "richResponse": {
            "items": [
            {
                "simpleResponse": {
                "textToSpeech": "failed to log todays weight"
                }
            }
            ]
        }
        }
    }
    }

failed_to_add_weight_resp = json.dumps(failed_to_add_weight)

def main(request):
    req_data = request.get_json()
    print (req_data)
    if 'queryResult' not in req_data:
        b = print('invalid input')
        return b

    usrWeight =str(req_data['queryResult']['parameters']['unit-weight']["amount"])
    print('user input is ' + usrWeight)

    usrName = req_data['queryResult']['parameters']['userName']
    print('user name is ' + usrName)
    
    try:
        app.insertTodb(usrWeight,usrName)
    except Exception as ex: #pylint: disable=broad-except
        print (ex)
        return failed_to_add_weight_resp

    weight_intent_resp = {
    "payload": {
        "google": {
        "expectUserResponse": "true",
        "richResponse": {
            "items": [
            {
                "simpleResponse": {
                "textToSpeech": "Great! your today's weight " + usrWeight + " is logged"
                }
            }
            ]
        }
        }
    }
    }

    weight_intent_resp_ga = json.dumps(weight_intent_resp)
    return weight_intent_resp_ga

