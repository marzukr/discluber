# -*- coding: utf-8 -*-

# from ClubEngine import tfidfEngine, twitterUtil, config
import tfidfEngine, twitterUtil, config

from pymongo import MongoClient
client = MongoClient()
db = client.clubsDatabase

# from pyelasticsearch import ElasticSearch
import requests
import json

from collections import Counter

from tqdm import tqdm

# es = ElasticSearch()
currentDataBaseTerm = "dva" # Used: elvis, club, clubs, holahola, fourK, gold, diamond, mercury, dva
baseURL = "http://localhost:9200/"
currentURL = baseURL + currentDataBaseTerm + "/tweets" # DO NOT USE A "/" AT THE END

def returnResults(user):
    # Gather the last 200 tweets of the user and combine them into a string
    userTweets = twitterUtil.getTweets(user, config.getConfig("tweetsPerUser"))

    #Take the combined tweet string and feed it into elastic search, then make the result into a pretty list of clubs
    sortedArray = formatSearch(uri=currentURL + "/_search?", term=userTweets, maxClubs=config.getConfig("clubsToReturn"))

    #Get the profile image URLS for the clubs and reorganize the data
    clubData = []
    for club in sortedArray:
        clubHandle = config.dbCol("followersList").find_one({"Club Name": club})["Twitter Account"]
        # clubHandle = "realdonaldtrump"
        clubImageURL = twitterUtil.getImageURL(clubHandle)
        newClubDataObject = {"name": club, "handle": clubHandle, "imageURL": clubImageURL}
        clubData.append(newClubDataObject)

    #Get results from the TFIDF engine
    formattedTerms = tfidfEngine.tokenResults(userTweets, [tfidfEngine.Token.TERM], config.getConfig("tokensToReturn"), config.dbCol(config.Collections.TOKENS))
    
    return {"clubs": clubData, "terms": formattedTerms}

"""====>ELASTICSEARCH<===="""
"""====>ELASTICSEARCH<===="""
"""====>ELASTICSEARCH<===="""
"""====>ELASTICSEARCH<===="""

# Get the elasticsearch url
def elasticsearchURL(date=config.getConfig("coDate")):
    return baseURL + date + "/tweets" # DO NOT USE A "/" AT THE END

#Take the term and run it through elasticsearch - simple elastic search query
def search(uri, term):
    query = json.dumps({
        "query": {
            "match": {
                "Tweets": term
            }
        }
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return results

# Search elasticsearch and makes it into a list of maxClubs clubs in order
def formatSearch(uri, term, maxClubs):
    results = search(uri, term)

    #LOOK INTO THIS TO OPTIMIZE RESULTS
    data = [doc for doc in results['hits']['hits']]

    prettyA = []
    for doc in data:
        # pretty = (doc['_source']["Club Name"], "test")
        pretty = doc['_source']["Club Name"]
        prettyA.append(pretty)
    return [x[0] for x in Counter(prettyA).most_common(maxClubs)]

# Add a document to elasticsearch
def create_doc(uri, doc_data):
    query = json.dumps(doc_data)
    response = requests.post(uri, data=query)
    return response

"""====>MONGODB<===="""
"""====>MONGODB<===="""
"""====>MONGODB<===="""
"""====>MONGODB<===="""

# Calculate and store the document frequencies of the given tweets in the given mongo collection
def storeDocumentFreq(date):
    #Get the tweets from the database and find tokens and their document frequencies
    tokenCounter = Counter()
    pbar = tqdm(total=config.dbCol(config.Collections.CLUB_DATA, coDate=date).count(), desc="    Getting tokens (1/2)")
    for clubItem in config.dbCol(config.Collections.CLUB_DATA, coDate=date).find({}):
        tokens = []
        for tweetAgg in clubItem["tweets"]:
            tokens += tfidfEngine.preprocess(tweetAgg, True)
        uTokens = list(set(tokens))
        tokenCounter.update(uTokens)

        pbar.update(1)
    pbar.close()

    #Store the tokens and their frequencies in mongo
    pbar = tqdm(total=len(tokenCounter), desc="    Adding to database (2/2)")
    tokenCollection = config.dbCol(config.Collections.TOKENS, coDate=date)
    for token, freq in tokenCounter.items():
        tokenCollection.insert_one({"Term": token, "df": freq})
        pbar.update(1)
    pbar.close()

# Faster internet could speed this?
def addClubMongo(clubName, twitterAccount, date):
    #Get club's followers, and their tweets
    followerTweets = twitterUtil.getFollowerTweets(twitterAccount)
    tweets = list(followerTweets.values())
    followers = list(followerTweets.keys())

    #Store the data in mongo
    config.dbCol(config.Collections.CLUB_DATA, coDate=date).insert_one({
        "twitterAccount": twitterAccount,
        "clubName": clubName,
        "tweets": tweets,
        "followers": followers,
        "followerTweets": followerTweets,
    })

# Run addClubMongo for every club in the config
def addNewClubs(date):
    clubs = {**config.getConfig("clubs")}
    total = len(clubs)
    prog = 0
    for account, name in clubs.items():
        addClubMongo(name, account, date)
        prog += 1
        print(int(prog/total*10000)/100,"%", sep='')

# Get and store follower data from the club data
def storeFollowerData(date):
    pbar = tqdm(total=config.dbCol(config.Collections.CLUB_DATA, coDate=date).count(), desc="    Store Follower Data")
    followerCollection = config.dbCol(config.Collections.FOLLOWER_DATA, coDate=date)
    for clubItem in config.dbCol(config.Collections.CLUB_DATA, coDate=date).find({}):
        twitterAccount = clubItem["twitterAccount"]
        clubName = clubItem["clubName"]
        for follower, tweets in clubItem["followerTweets"].items():
            followerCollection.insert_one({
                "twitterAccount": twitterAccount,
                "clubName": clubName,
                "tweets": tweets,
                "follower": follower,
            })
        pbar.update(1)
    pbar.close()