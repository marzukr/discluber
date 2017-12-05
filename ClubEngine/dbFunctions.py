# import tfidfEngine, twitterUtil
from ClubEngine import tfidfEngine, twitterUtil

from pymongo import MongoClient
client = MongoClient()
db = client["clubsDatabase"]
configCollection = db["config"]

from tqdm import tqdm
from collections import Counter

import csv

# from timeit import default_timer as timer

def getConfig(key):
    return configCollection.find_one()[key]

# Calculate and store the document frequencies of the given tweets in the given mongo collection
def storeDocumentFreq(tweetCollection, freqCollection):
    #Get the tweets from the database and find tokens and their document frequencies
    tokenCounter = Counter()
    pbar = tqdm(total=tweetCollection.count(), desc="    Getting tokens")
    for clubItem in tweetCollection.find({}):
        tokens = []
        for tweetAgg in clubItem["TweetsString"]:
            tokens += tfidfEngine.preprocess(tweetAgg, True)
        uTokens = list(set(tokens))
        tokenCounter.update(uTokens)

        pbar.update(1)
    pbar.close()

    #Store the tokens and their frequencies in mongo
    pbar = tqdm(total=len(tokenCounter), desc="    Adding to database")
    for token, freq in tokenCounter.items():
        freqCollection.insert_one({"Term": token, "df": freq})
        pbar.update(1)
    pbar.close()

# Faster internet could speed this?
def addClubMongo(clubName, twitterAccount, tweetCollection, twitterAPI):
    #Get config parameters
    maxTweets = getConfig("tweetsPerFollower")
    maxFollowers = getConfig("followersPerClub")

    #Get club's followers, and their tweets
    tweets = []
    followers = []
    followerTweets = {}
    pbar = tqdm(total=maxFollowers, desc="    Adding " + clubName)
    for follower in twitterUtil.getFollowers(twitterAccount, twitterAPI):
        userTweets = twitterUtil.getTweets(follower, maxTweets, twitterAPI)
        if userTweets is not None and userTweets != "":
            tweets.append(userTweets)
            followers.append(follower)
            followerTweets[follower] = userTweets
            pbar.update(1)
        if len(followers) >= maxFollowers:
            break
    pbar.close()

    #Store the data in mongo
    tweetCollection.insert_one({
        "twitterAccount": twitterAccount,
        "clubName": clubName,
        "tweets": tweets,
        "followers": followers,
        "followerTweets": followerTweets,
    })

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
