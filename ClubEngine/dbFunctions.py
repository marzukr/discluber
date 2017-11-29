import tfidfEngine

import tweepy
from pymongo import MongoClient
client = MongoClient()
db = client["clubsDatabase"]
configCollection = db["config"]

from tqdm import tqdm
from collections import Counter

from timeit import default_timer as timer

def getConfig(key):
    return configCollection.find_one()[key]

#Calculate and store the document frequencies of the given tweets in the given mongo collection
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

def getFollowers(twitterAccount, twitterAPI):
    followersPages = tweepy.Cursor(twitterAPI.followers, screen_name=twitterAccount).items()
    followersTwitters = (user.screen_name for i, user in enumerate(followersPages))
    return followersTwitters

#There appears to be a significant delay between some iterations of the cursor, faster internet could help?
def getTweets(twitterAccount, maxTweets, twitterAPI):
    try:
        tweetCursor = tweepy.Cursor(twitterAPI.user_timeline, screen_name=twitterAccount).items(limit=maxTweets)
        tweets = [tweet.text for i, tweet in enumerate(tweetCursor)]
        return " ".join(tweets)
    except tweepy.error.TweepError:
        return None

#Faster internet could speed this?
def addClubMongo(clubName, twitterAccount, tweetCollection, twitterAPI):
    #Get config parameters
    maxTweets = getConfig("tweetsPerFollower")
    maxFollowers = getConfig("followersPerClub")

    tweets = []
    followers = []
    followerTweets = {}
    pbar = tqdm(total=maxFollowers, desc="    Adding " + clubName)
    for follower in getFollowers(twitterAccount, twitterAPI):
        userTweets = getTweets(follower, maxTweets, twitterAPI)
        if userTweets is not None and userTweets != "":
            tweets.append(userTweets)
            followers.append(follower)
            followerTweets[follower] = userTweets
            pbar.update(1)
        if len(followers) >= maxFollowers:
            break
    pbar.close()

    tweetCollection.insert_one({
        "twitterAccount": twitterAccount,
        "clubName": clubName,
        "tweets": tweets,
        "followers": followers,
        "followerTweets": followerTweets,
    })