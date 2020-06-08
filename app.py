import json
import pymongo
from datetime import datetime

#decalre db client
client = pymongo.MongoClient("mongodb+srv://smart_weight_tracker:2HK7CFMrobkE1ybY@cluster0-5yoef.gcp.mongodb.net/test?retryWrites=true&w=majority")
db=client.smart_weight_tracker

today = datetime.today()
# atlas_user = "smart_weight_tracker"
# atlas_pass = "2HK7CFMrobkE1ybY"

def insertWeight(usrWeight,usrName):
    insertWeight = {
    "date" : today,
    "name" : usrName,
    "weight" : usrWeight
    }
    #call to insert user weight and name with todays date in db
    db.weightLog.insert_one(insertWeight)

def fetchLastLog(usrName):


