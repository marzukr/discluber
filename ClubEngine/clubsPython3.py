# from ClubEngine import tfidfEngine, twitterUtil, config
import tfidfEngine, twitterUtil, config

from pymongo import MongoClient
# client = MongoClient(host="mongodb://mongo:27017")
client = MongoClient(host="localhost:27017")
db = client.clubsDatabase

esURL = "http://localhost:9200/" # Development
# esURL = "http://elasticsearch:9200/" # Docker Production

import requests
import json

from collections import Counter

from tqdm import tqdm

import time
import csv

def returnResults(user):
    # Gather the last 200 tweets of the user and combine them into a string
    tweetTime = time.time()
    userTweets = twitterUtil.getTweets(user, config.getConfig("tweetsPerUser"))
    totalTweetTime = time.time() - tweetTime

    #Take the combined tweet string and feed it into elastic search, then make the result into a pretty list of clubs
    searchTime = time.time()
    clubData = formatSearch(uri=elasticsearchURL() + "/_search?", term=userTweets, maxClubs=config.getConfig("clubsToReturn"))
    totalSearchTime = time.time() - searchTime

    #Get results from the TFIDF engine
    tokenTime = time.time()
    formattedTerms = tfidfEngine.tokenResults(userTweets, [tfidfEngine.Token.TERM, tfidfEngine.Token.HASHTAG, tfidfEngine.Token.USER], config.getConfig("tokensToReturn"), config.dbCol(config.Collections.TOKENS))
    totalTokenTime = time.time() - tokenTime

    # print("tweet:", str(totalTweetTime) + "s")
    # print("search:", str(totalSearchTime) + "s")
    # print("token:", str(totalTokenTime) + "s")
    
    return {"clubs": clubData, "terms": formattedTerms}

"""
====>ELASTICSEARCH<====
====>ELASTICSEARCH<====
====>ELASTICSEARCH<====
====>ELASTICSEARCH<====
"""

# Get the elasticsearch url
def elasticsearchURL(date=config.getConfig("coDate")):
    # Used: elvis, club, clubs, holahola, fourK, gold, diamond, mercury, dva
    return esURL + date + "/tweets" # DO NOT USE A "/" AT THE END

#Take the term and run it through elasticsearch - simple elastic search query
def search(uri, term):
    # query = json.dumps({
    #     "query": {
    #         "match": {
    #             "tweets": term
    #         }
    #     }
    # })
    query = {
        "query": {
            "match": {
                "tweets": term
            }
        }
    }
    response = requests.get(uri, json=query)
    results = json.loads(response.text)
    return results

# Search elasticsearch and makes it into a list of maxClubs clubs in order
def formatSearch(uri, term, maxClubs):
    results = search(uri, term)
    try:
        #LOOK INTO THIS TO OPTIMIZE RESULTS
        data = [doc for doc in results['hits']['hits']]

        prettyA = []
        for doc in data:
            # pretty = (doc['_source']["Club Name"], "test")
            docData = doc['_source']
            clubImageURL = twitterUtil.getImageURL(docData["twitterAccount"])
            pretty = (docData["clubName"], docData["twitterAccount"], clubImageURL) # Tuple (clubName, twitterAccount, clubImageURL)
            prettyA.append(pretty)
        topClubs = [x[0] for x in Counter(prettyA).most_common(maxClubs)]
        formattedData = []
        for club in topClubs:
            formattedData.append({"name": club[0], "handle": club[1], "imageURL": club[2]})
        return formattedData
    except KeyError:
        return []

# Add a document to elasticsearch
def create_doc(uri, doc_data):
    # query = json.dumps(doc_data)
    response = requests.post(uri, json=doc_data)
    return response

# Add the follower data to elasticsearch
def addFollowerDataES(dateD):
    esURL = elasticsearchURL(date=dateD)
    pbar = tqdm(total=config.dbCol(config.Collections.FOLLOWER_DATA, coDate=dateD).count(), desc="    Adding to ES")
    for followerItem in config.dbCol(config.Collections.FOLLOWER_DATA, coDate=dateD).find({}):
        if followerItem["twitterAccount"] != "thedailynu": # dailyNU removed
            modifyData = followerItem.copy()
            modifyData.pop("_id", None) # Remove the "_id" property that Mongo adds
            create_doc(esURL, modifyData)
            pbar.update(1)
    pbar.close()

"""
====>MONGODB<====
====>MONGODB<====
====>MONGODB<====
====>MONGODB<====
"""

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

"""
====>VALIDATION<====
====>VALIDATION<====
====>VALIDATION<====
====>VALIDATION<====
"""

# Retrieves accounts that are not part of the model for each club, tends to crash after a few accounts
def getTestFollowers():
    #Store all the club twitter account and follwer in an array
    clubCollection = config.dbCol(config.Collections.CLUB_DATA)
    validationCollection = config.dbCol(config.Collections.VALIDATION2)

    clubs = []
    for club in clubCollection.find({"doneFlag": {"$exists": False}}):
        clubs.append((club["twitterAccount"], club["followers"], club["testers"], club["testers2"]))
    pbar = tqdm(total=len(clubs), desc="    Validate Test Users")
    #Loop through each club and get the test accounts
    for club in clubs:
        twitterAccount = club[0]
        followers = club[1]
        testers = club[2]
        testers2 = club[3]
        newTesters = []
        followersPages = None

        #Gets the tweepy cursor, tends to lose connection, crash, so inside try/except
        while True:
            try:
                followersPages = twitterUtil.getFollowers(twitterAccount)
                break
            except:
                pass
        
        #Test each follower to see if in model or is blank/protected, if not, add them to testers
        for followerItem in followersPages:
            testFollower = followerItem.screen_name
            if testFollower not in testers and testFollower not in followers:
                clubs = returnResults(testFollower)["clubs"]
                results = [club["handle"] for club in clubs]
                if len(results) >= 3:
                    newTesters.append((testFollower, results))
                    if len(testers2) + len(newTesters) >= 100:
                        break

        #Add the testers into mongo
        validationDocuments = []
        testFollowers = []
        for tester in newTesters:
            validationData = {"tester": tester[0], "twitterAccount": twitterAccount, "results": tester[1]}
            validationDocuments.append(validationData)
            testFollowers.append(tester[0])
        if len(testFollowers) != 0:
            validationCollection.insert(validationDocuments)
        clubCollection.update({"twitterAccount": twitterAccount}, {"$set": {"testers2": testFollowers+testers2, "doneFlag": "foo"}})
        pbar.update(1)
    pbar.close()

def transferValidation():
    clubCollection = config.dbCol(config.Collections.CLUB_DATA)
    validation1 = config.dbCol(config.Collections.VALIDATION)
    validation2 = config.dbCol(config.Collections.VALIDATION2)

    validations = []
    for tester in validation1.find():
        if tester["tester"] in clubCollection.find_one({"twitterAccount": tester["twitterAccount"]})["testers2"]:
            validations.append(tester)
    validation2.insert(validations)

# Get and store validation data from the club data
def storeValidationData(vCol):
    clubCollection = config.dbCol(config.Collections.CLUB_DATA)
    validationCollection = config.dbCol(vCol)
    clubs = []
    for club in clubCollection.find():
        clubs.append((club["twitterAccount"], club["testers"]))
    validationData = []
    for club in clubs:
        for tester in club[1]:
            # if club[0] != "thedailynu": #dailyNU removed
            validationData.append({"tester": tester, "twitterAccount": club[0]})
    validationCollection.insert(validationData)

def validate(vCol):
    validationCollection = config.dbCol(vCol)
    pbar = tqdm(total=validationCollection.count({"results": {"$exists": False}}), desc="    Validate Each User")
    for tester in validationCollection.find({"results": {"$exists": False}}).batch_size(20):
        clubs = returnResults(tester["tester"])["clubs"]
        results = [club["handle"] for club in clubs]
        mongoID = tester["_id"]
        validationCollection.update({"_id": mongoID}, {"$set": {"results": results}})
        pbar.update(1)
    pbar.close()

def calculateValidations(collection):
    correct3 = 0
    correct2 = 0
    correct1 = 0
    for tester in config.dbCol(collection).find():
        if tester["twitterAccount"] in tester["results"][:3]:
            correct3 += 1
            if tester["twitterAccount"] in tester["results"][:2]:
                correct2 += 1
                if tester["twitterAccount"] in tester["results"][:1]:
                    correct1 += 1
    totalCount = config.dbCol(collection).count()
    print("Correct1: {}".format(correct1/totalCount))
    print("Correct2: {}".format(correct2/totalCount))
    print("Correct3: {}".format(correct3/totalCount))

def clubAccuracy():
    accuracy = {}
    for club in config.dbCol(config.Collections.CLUB_DATA).find():
        accuracy[club["twitterAccount"]] = {"c1": 0, "c2": 0, "c3": 0, "total": 0}
    for tester in config.dbCol(config.Collections.VALIDATION).find():
        if tester["twitterAccount"] in tester["results"][:3]:
            accuracy[tester["twitterAccount"]]["c3"] += 1
            if tester["twitterAccount"] in tester["results"][:2]:
                accuracy[tester["twitterAccount"]]["c2"] += 1
                if tester["twitterAccount"] in tester["results"][:1]:
                    accuracy[tester["twitterAccount"]]["c1"] += 1
        accuracy[tester["twitterAccount"]]["total"] += 1
    for club in accuracy:
        accuracy[club]["c1"] = accuracy[club]["c1"] / accuracy[club]["total"]
        accuracy[club]["c2"] = accuracy[club]["c2"] / accuracy[club]["total"]
        accuracy[club]["c3"] = accuracy[club]["c3"] / accuracy[club]["total"]
    print(accuracy)
    
def testerCount():
    for tester in config.dbCol(config.Collections.CLUB_DATA).find():
        print("{}".format(len(tester["testers"])))

def removeKey(collection, key):
    collection.update({}, {"$unset": {key: 1}}, multi=True)

def replaceValue(collection, key, value, newValue):
    mCollection = config.dbCol(collection)
    for entry in mCollection.find():
        if entry[key] == value:
            mCollection.update({"_id": entry["_id"]}, {"$set": {key: newValue}})

def find_duplicates():
    model_collection = config.dbCol(config.Collections.CLUB_DATA)
    followers = []
    for c in model_collection.find():
        for f in c["followers"]:
            followers.append(f)
    c = Counter(followers)
    duplicate = 0
    for i in c:
        if c[i] > 1:
            duplicate += 1
    print(duplicate)
    print(len(c))
    # print(c.most_common(10))

# storeValidationData("validation5")
