from pymongo import MongoClient
# client = MongoClient(host="mongodb://mongo:27017")
client = MongoClient(host="localhost:27017")
db = client["clubsDatabase"]
configCollection = db["config"]

import csv
from enum import Enum
class Collections(Enum):
    CONFIG = "config"
    CLUB_DATA = "clubData"
    FOLLOWER_DATA = "followerData"
    TOKENS = "tokens"
    VALIDATION = "validation"
    VALIDATION2 = "validation2"

def getConfig(key):
    return configCollection.find_one()[key]

# Open CSV file and store clubs in config collection in database
def storeCSV_Config(filename):
    with open(filename, "r") as csvFile:
        csvReader = csv.reader(csvFile)
        next(csvReader)
        for club in csvReader:
            try:
                if club[5] == "1":
                    configCollection.update_one({}, {"$set": {"clubsFull."+club[1]: club[0]}})
            except IndexError:
                continue

def dbCol(collectionType, coDate=getConfig("coDate")):
    return db[collectionType.value + "_" + coDate]