import json
import pymongo
import datetime
import os

mongodb_user = os.environ['MONGODB_USER']
mongodb_password = os.environ['MONGODB_PASSWORD']
mongodb_string="mongodb+srv://" + mongodb_user + ":" + mongodb_password + "@cluster0-5yoef.mongodb.net/smart_weight_tracker?retryWrites=true&w=majority"

# https://pymongo.readthedocs.io/en/stable/api/pymongo/cursor.html#pymongo.cursor.CursorType.EXHAUST
#decalre db client
client = pymongo.MongoClient(mongodb_string)
db = client.smart_weight_tracker

def insertWeight(usrWeight,usrName):
    userWeight = int(usrWeight)
    userName = usrName.lower()
    todaysdate = datetime.datetime.today()
    insertWeight = {
    "date" : todaysdate,
    "name" : userName,
    "weight" : userWeight
    }
    #call to insert user weight and name with todays date in db
    db.weightLog.insert_one(insertWeight)

def fetchLastLog(usrName):
    userName = usrName.lower()
    myCursor=db.weightLog.find({"name":userName}).sort('date',pymongo.DESCENDING).limit(1)
    if myCursor.count() == 0 : 
        respMsg = "I dont think you have started loging weight here. You can start today!" 
        return respMsg
    for doc in myCursor:
        print(doc)
        last_weight=str(doc['weight'])
        respMsg = "Your last weight logged was " + last_weight + " kilogram. Is there anything else that I can do for you?" 
    return respMsg


def caluculate_diff(userName,period):
    userName = userName.lower()
    period = int(period)
    mostRecentLog = db.weightLog.find({"name":userName}).sort('date',pymongo.DESCENDING).limit(1)
    if mostRecentLog.count() == 0:
        print("mostrecent log not found")
        return {
            "amount" : "unknown",
            "result" : "Sorry, I do not have sufficient data needed" 
        }
    for log in mostRecentLog:
        print(log)
        mostRecentweightLog = log['weight']
        
    # todaysDate = datetime.date.today()
    lastdate = datetime.date.today() - datetime.timedelta(days=period)
    day = int(lastdate.strftime("%d"))
    year= int(lastdate.strftime("%Y"))
    month = int(lastdate.strftime("%m"))
    #find out lastdate with time as 12 AM or 00:00:00 
    # lastdate = datetime.datetime(year, month, day)
    #check data for lastdate
    myCursor = db.weightLog.find({"name":userName,
                                  "date" : {
                                      '$lte' : datetime.datetime(year, month, day+1),
                                      '$gte' : datetime.datetime(year, month, day)
                                    }
                                }).sort("date",pymongo.ASCENDING).limit(1)

    if myCursor.count() == 0:
        print("data not found for 1 day")
        myCursor = db.weightLog.find({"name":userName,
                                  "date" : {
                                      '$lte' : datetime.datetime(year, month, day+5),
                                      '$gte' : datetime.datetime(year, month, day-5)
                                    }
                                }).sort("date",pymongo.ASCENDING).limit(1)
        if myCursor.count() == 0:
            print("data not found for 10 days")
            return {
            "amount" : "unknown",
            "result" : "Sorry, I do not have sufficient data needed" 
        }
    
    for doc in myCursor:
        print(doc)
        oldWeightLog = doc['weight']

    weight_diff = oldWeightLog - mostRecentweightLog
    print("weight diff is " + str(weight_diff))
    if float(weight_diff) > 0 : 
        outMsg = {
            "amount" : weight_diff,
            "result" : "lost" 
        }
    else :
        outMsg = {
            "amount" : -weight_diff,
            "result" : "gain" 
        }
    print(outMsg)
    return outMsg

    '''logic, fetch records for days user has requested. 
    sort by date and pick the first  record for as most recent weght log
    find out the lastdate based on period that user is asking and check if you have data for that day. if not found
    run loop for 5 days plus and 5 days minus and if not found find the 1st record that user ever entered
    and tell user that i couldn't find sufficient data but you hv lost/gained this much since inception 

    calculate the difference and based on positive or negative result 
    return msg with weight diffrence and motivational message
    '''



