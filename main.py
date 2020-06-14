import app
import json

ga_response = {
    "payload": {
        "google": {
        "expectUserResponse": True,
        "richResponse": {
            "items": [
            {
                "simpleResponse": {
                "textToSpeech": "null"
                }
            }
            ]
        }
        }
    }
    }

def handler(event, context):
    print(json.dumps(event))
    # req_data = json.loads(event['body'])
    # req_data = event

    if 'queryResult' not in event:
        print('invalid input')
        textToSpeech = "This is an invalid input."
        ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
        return ga_response

    if event['queryResult']['intent']['displayName'] == "user_weight" : 
        usrWeight = event['queryResult']['parameters']['unit-weight']["amount"]
        # print('user input is ' + str(usrWeight))
        usrName = event['queryResult']['parameters']['userName']
        # print('user name is ' + usrName)
        
        try:
            app.insertWeight(usrWeight,usrName)
        except Exception as ex: #pylint: disable=broad-except
            print (ex)
            textToSpeech = "I am unable to add this log, Please try again later"
            ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
            return ga_response

        textToSpeech = "Great! your today's weight " + str(usrWeight) + " is logged. Is there anything else that I can do for you?" 
        ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
        return ga_response


    elif event['queryResult']['intent']['displayName'] == "last_weight_log":
        usrName = event['queryResult']['parameters']['userName']
        try:
            last_log = app.fetchLastLog(usrName)
        except Exception as ex: #pylint: disable=broad-except
            print (ex)
            textToSpeech = "Oh oo, I am unable to fetch last log, Please try again later"
            ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
            return ga_response
    
        textToSpeech = "Your last weight logged was " + last_log + " kilogram. Is there anything else that I can do for you?" 
        ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
        return ga_response

    elif event['queryResult']['intent']['displayName'] == "weight_change":
        usrName = event['queryResult']['parameters']['userName']
        period = str(event['queryResult']['parameters']['change_period'])

        try:
            weight_result = app.caluculate_diff(usrName,period)
        except Exception as ex: #pylint: disable=broad-except
            print (ex)
            textToSpeech = "Sorry, I do not have sufficient data needed"
            ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
            return ga_response

        if weight_result['amount'] == "unknown":
            textToSpeech = weight_result['result']
        else:
            if weight_result['result'] == "gain":
                textToSpeech = usrName.capitalize() + ", You have gained " + str(weight_result['amount']) + " kilogram in last " + period + " days. Thank you for using Smart weight tracker"
            else:
                textToSpeech = "Hoorah, You have lost " + str(weight_result['amount']) + " kilogram in last " + period + " days.Keep it going. Thank you for using Smart weight tracker"
        ga_response['payload']['google']['expectUserResponse'] = False
        ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
        return ga_response
    

