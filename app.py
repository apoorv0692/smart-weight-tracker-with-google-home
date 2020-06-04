import pymongo
from datetime import datetime

#decalre db client
client = pymongo.MongoClient("mongodb+srv://smart_weight_tracker:2HK7CFMrobkE1ybY@cluster0-5yoef.gcp.mongodb.net/test?retryWrites=true&w=majority")
db=client.smart_weight_tracker

today = datetime.today()
# atlas_user = "smart_weight_tracker"
# atlas_pass = "2HK7CFMrobkE1ybY"

#function to insert user weight with todays date in db
def insertTodb(usrWeight,usrName):
    
    insertWeight = {
    "Date" : today,
    "Name" : usrName,
    "weight" : usrWeight
    }

    db.weightLog.insert_one(insertWeight)

