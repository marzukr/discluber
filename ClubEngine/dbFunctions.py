from ClubEngine import tfidfEngine

import tweepy
from pymongo import MongoClient
client = MongoClient()
db = client["clubsDatabase"]

from tqdm import tqdm
from collections import Counter

#Calculate and store the document frequencies of the given tweets in the given mongo collection
def storeDocumentFreq(tweetCollection, freqCollection):
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

    pbar = tqdm(total=len(tokenCounter), desc="    Adding to database")
    for token, freq in tokenCounter.items():
        freqCollection.insert_one({"Term": token, "df": freq})
        pbar.update(1)
    pbar.close()

# def function():
#     none = None

def getFollowers(twitterAccount, maxUsers, twitterAPI):
    followersPages = tweepy.Cursor(twitterAPI.followers_ids, screen_name=twitterAccount).items(limit=maxUsers)
    followersTwitters = [user.screen_name for i, user in enumerate(followersPages)]
    return followersTwitters

def addClubMongo(clubConfig, tweetCollection, twitterAPI):
    followers = getFollowers(clubConfig["twitterAccount"], 200, twitterAPI)
