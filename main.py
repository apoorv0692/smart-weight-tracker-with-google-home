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
        ga_response['payload']['google']['expectUserResponse'] = False
        return ga_response

    if event['queryResult']['intent']['displayName'] == "user_weight" or event['queryResult']['intent']['displayName'] == "last_weight_log - yes": 
        usrWeight = event['queryResult']['parameters']['unit-weight']["amount"]
        # print('user input is ' + str(usrWeight))
        usrName = event['queryResult']['parameters']['userName']
        # print('user name is ' + usrName)
        
        try:
            app.insertWeight(usrWeight,usrName)
        except Exception as ex: #pylint: disable=broad-except
            print (ex)
            textToSpeech = "I am unable to add this log, Please try again later"
            ga_response['payload']['google']['expectUserResponse'] = False
            ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
            return ga_response

        textToSpeech = "Great! your today's weight " + str(usrWeight) + " Kilograms is logged. Is there anything else that I can do for you?" 
        ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
        ga_response['payload']['google']['expectUserResponse'] = True
        return ga_response


    elif event['queryResult']['intent']['displayName'] == "last_weight_log":
        usrName = event['queryResult']['parameters']['userName']
        try:
            last_log = app.fetchLastLog(usrName)
        except Exception as ex: #pylint: disable=broad-except
            print (ex)
            textToSpeech = "Oh oo, I am unable to fetch last log, Please try again later"
            ga_response['payload']['google']['expectUserResponse'] = False
            ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
            return ga_response
    
        ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = last_log['textResp']
        ga_response['payload']['google']['expectUserResponse'] = last_log['expectUserResponse']
        return ga_response

    elif event['queryResult']['intent']['displayName'] == "weight_change - yes":
        usrName = event['queryResult']['parameters']['userName']
        period = str(event['queryResult']['parameters']['change_period'])

        try:
            weight_result = app.caluculate_diff(usrName,period)
        except Exception as ex: #pylint: disable=broad-except
            print (ex)
            textToSpeech = "Sorry, I do not have sufficient data needed, continue logging your weight for a few more days and you will be good to go. Thank you for using Smart Weight Tracker"
            ga_response['payload']['google']['expectUserResponse'] = False
            ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
            return ga_response

        if weight_result['amount'] == "unknown":
            textToSpeech = weight_result['result']
        else:
            if weight_result['result'] == "gain":
                textToSpeech = usrName.capitalize() + ", You have gained " + str(weight_result['amount']) + " kilogram in last " + period + " days. Thank you for using Smart weight tracker"
            elif weight_result['result'] == "lost":
                textToSpeech = "Hoorah, You have lost " + str(weight_result['amount']) + " kilogram in last " + period + " days.Keep it going. Thank you for using Smart weight tracker"
            else:
                textToSpeech = usrName.capitalize() +  ", You have not lost weight in " + period + " days.Keep it going. Thank you for using Smart weight tracker"
                
        ga_response['payload']['google']['expectUserResponse'] = False
        ga_response['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = textToSpeech
        return ga_response
    

