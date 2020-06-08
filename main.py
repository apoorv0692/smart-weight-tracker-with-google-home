import app
import json

ga_response = {
    "payload": {
        "google": {
        "expectUserResponse": "true",
        "richResponse": {
            "items": [
            {
                "simpleResponse": {
                "textToSpeech": ""
                }
            }
            ]
        }
        }
    }
    }

def main(request):
    req_data = request.get_json()
    print (req_data)

    if 'queryResult' not in req_data and 'intent' not in req_data :
        print('invalid input')
        textToSpeech = "Oh oo, This is an invalid input."
        ga_response['payload']['google']['richResponse']['items'][0]['textToSpeech'] = textToSpeech
        invalid_input_resp = json.dumps(ga_response)
        return invalid_input_resp

    if req_data['intent']['displayName'] == "User Weight" : 
        usrWeight = str(req_data['queryResult']['parameters']['unit-weight']["amount"])
        # print('user input is ' + usrWeight)

        usrName = req_data['queryResult']['parameters']['userName']
        # print('user name is ' + usrName)
        
        try:
            app.insertWeight(usrWeight,usrName)
        except Exception as ex: #pylint: disable=broad-except
            print (ex)
            textToSpeech = "Oh oo, I am unable to add this log, Is there anything else that i can do for you "
            ga_response['payload']['google']['richResponse']['items'][0]['textToSpeech'] = textToSpeech
            failed_to_add_weight_resp = json.dumps(ga_response)
            return failed_to_add_weight_resp

        textToSpeech = "Great! your today's weight " + usrWeight + " is logged. Is there anything else that i can do for you " + usrName 
        ga_response['payload']['google']['richResponse']['items'][0]['textToSpeech'] = textToSpeech
        weight_intent_resp_ga = json.dumps(ga_response)
        return weight_intent_resp_ga


    elif req_data['intent']['displayName'] == "last_weight_log" :
        try:
            app.fetchLastLog(usrName)
        except Exception as ex: #pylint: disable=broad-except
            print (ex)
            textToSpeech = "Oh oo, I am unable to fetch last log, Please try again later"
            ga_response['payload']['google']['richResponse']['items'][0]['textToSpeech'] = textToSpeech
            failed_to_add_weight_resp = json.dumps(ga_response)
            return failed_to_add_weight_resp
    else:
        #don nothing
    

