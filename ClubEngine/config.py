from pymongo import MongoClient
client = MongoClient()
db = client["clubsDatabase"]
configCollection = db["config"]

import csv
from enum import Enum
class Collections(Enum):
    CONFIG = "config"
    CLUB_DATA = "clubData"
    FOLLOWER_DATA = "followerData"
    TOKENS = "tokens"

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
                    configCollection.update_one({}, {"$set": {"clubs."+club[1]: club[0]}})
            except IndexError:
                continue

def dbCol(collectionType, coDate=getConfig("coDate")):
    return db[collectionType.value + "_" + coDate]
