# -*- coding: utf-8 -*-

from ClubEngine import tfidfEngine

from pymongo import MongoClient
client = MongoClient()
db = client.clubsDatabase
collection = db.followersList
tweetsCollection = db.tweetsList
tweetsUsers = db.tweetsUsers
tweetsUsersNew = db.tweetsUsersNew

documentCollection = db.documentCollection

# from elasticsearch import Elasticsearch, exceptions
from pyelasticsearch import ElasticSearch
import requests
import json
import tweepy

import time
# import sys
# import bson
import urllib.request
from bs4 import BeautifulSoup

from math import log

es = ElasticSearch()
currentDataBaseTerm = "dva" # Used: elvis, club, clubs, holahola, fourK, gold, diamond, mercury, dva
currentURL = "http://localhost:9200/" + currentDataBaseTerm + "/tweets" # DO NOT USE A "/" AT THE END

consumer_key = "LsAwFJvshsac0oV1MWPT5SPdP"
consumer_secret = "HtOBG7Lv66RUIvmtffEe5LYN0RRVncuQp7p1bXoyGdNu3coYkw"

access_key = "2183673402-AvddwhaVAuB8lngOqVbtX31kQMpnTnbfhSOs7iO"
access_secret = "1Ar33ZPEeyEOs1gdn7aZLYq5tTyW4E3JyQaQBJyo4gUzf"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def search(uri, term):
    """Simple Elasticsearch Query"""
    query = json.dumps({
        "query": {
            "match": {
                "Tweets": term
            }
        }
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    # print(results)
    return results

def mlt(uri, user):
    tweepyCursor = tweepy.Cursor(api.user_timeline, screen_name=user, count=200).items()
    hola = ""
    n = 0
    for tweet in tweepyCursor:
        hola = hola + tweet.text
        n = n + 1
        if n >= 200:
            break
    query = json.dumps({
        "query":
        {
            "more_like_this" :
            {
                "fields" : ["Tweets"],
                "like" : hola,
                "min_term_freq" : 1,
                "max_query_terms" : 12,
                "max_word_length" : 12
            }
        }
    })
    response = requests.get(uri, data=query)
    print("hola")
    results = json.loads(response.text)
    print("bob")
    print(results)

def format_results(results):
    """Print results nicely:
    doc_id) content
    """
    data = [doc for doc in results['hits']['hits']]
    prettyA = []
    for doc in data:
        # CHANGE THIS for different outputs
        pretty = "%s" % (doc['_source'] ['Club Name'])
        prettyA.append(pretty)
    return prettyA

def create_doc(uri, doc_data):
    """Create new document."""
    query = json.dumps(doc_data)
    response = requests.post(uri, data=query)
    print(response)

# create_doc(uri="http://localhost:9200/elvis/tweets", doc_data={"Club Name": "NU Democrats", "hola": "hola"})

# king = search(uri="http://localhost:9200/elvis/tweets/_search?", term=hola)
# print(format_results(results=king))
# print(king)

def newIndex():
    cursor = tweetsUsers.find({})
    for item in cursor:
        dataToSearch = {"Tweets": item["Tweets"], "Club Name": item["Club Name"]}
        print(item["Club Name"])
        create_doc(uri=currentURL, doc_data=dataToSearch)

def returnResults(user):
    # Gather the last 200 tweets of the user and combine them into a string
    tweepyCursor = tweepy.Cursor(api.user_timeline, screen_name=user, count=200).items()
    userTweets = ""
    n = 0
    for tweet in tweepyCursor:
        userTweets = userTweets + tweet.text
        n = n + 1
        if n >= 200:
            break
    print(userTweets)
    exit()
    
    userList = tfidfEngine.freqCount(userTweets, True)

    king = search(uri=currentURL + "/_search?", term=userList)

    points = []
    uPoints = []
    uniqueClubs = []

    clubsArray = format_results(results=king)
    for n in range(0,len(clubsArray)):
        points.append(len(clubsArray) - n)
    for club in clubsArray:
        if club not in uniqueClubs:
            uniqueClubs.append(club)
    for uClub in uniqueClubs:
        for rClub in clubsArray:
            if rClub == uClub:
                uIndex = uniqueClubs.index(uClub)
                index = clubsArray.index(rClub)
                if 0 <= uIndex < len(uPoints):
                    uPoints[uIndex] = uPoints[uIndex] + points[index]
                else:
                    uPoints.append(points[index])
    sortedArray = [x for (y, x) in sorted(zip(uPoints, uniqueClubs), reverse=True)]

    #calculate TFIDF stuff here
    listWithCounts = tfidfEngine.freqCount(userList, False)
    totalTermCount = 0
    for item in listWithCounts:
        totalTermCount += item[1]

    tfidfArray = []
    for i in range(0,len(listWithCounts)-1):
        term = listWithCounts[i][0].lower()
        documentCollecData = documentCollection.find_one({'Term': term})
        if documentCollecData is not None:
            tf = listWithCounts[i][1]/totalTermCount
            df = 50/documentCollecData["df"]
            tfidfCalc = tf * log(df)
            arrayObject = (term, tfidfCalc)
            tfidfArray.append(arrayObject)
        else:
            continue
    tfidfArray.sort(key=lambda tup: tup[1], reverse=True)
    if len(tfidfArray) >= 5:
        tfidfArray = tfidfArray[0:5]

    return [sortedArray, tfidfArray]

def addTwitterUser(user, clubName):
    followersCursor = tweepy.Cursor(api.followers, screen_name=user, count=300).items()
    fabio = []
    for fob in followersCursor:
        fabio.append(fob.screen_name)
        if len(fabio) >= 200:
            break
    followers = []
    clubTweets = []
    for followerH in fabio:
        follower = followerH
        url = "https://twitter.com/%s" % follower
        tweetConCat = ""
        tweetsA = []
        try:
            with urllib.request.urlopen(url) as url:
                f = url.read()
        #urllib.error.HTTPError as e
        except:
            print("Skipping(1) " + follower)
            continue
        soup = BeautifulSoup(f, 'html.parser')
        def do_it():
            print("Adding %s Tweets" % follower)
            tweepyCursor = tweepy.Cursor(api.user_timeline, screen_name=follower, count=200).items()
            for tweet in tweepyCursor:
                hola = tweet.text
                tweetsA.append(hola)
                if len(tweetsA) >= 200:
                    break
        if soup.findAll("h2", { "class" : "ProtectedTimeline-heading" }) != [] or soup.findAll("div", {"class": "body-content"}) != [] or soup.findAll("div", {"class": "flex-module error-page clearfix"}) != []:
            print("Skipping(2) " + follower)
            continue
        else:
            try:
                do_it()
            except tweepy.error.TweepError as e:
                print("Exception")
                time.sleep(60*15)
                print("Out-waited exception")
                do_it()
            for objectT in tweetsA:
                tweetConCat = tweetConCat + objectT
        followers.append(follower)
        clubTweets.append(tweetConCat)
        if len(followers) >= 200:
            break
    data = {"Club Name": clubName, "Twitter Account": user, "Followers": followers}
    data2 = {"Club Name": clubName, "Twitter Account": user, "Followers": followers, "TweetsString": clubTweets}
    # RE ENABLE FOR REGULAR USE #
    # collection.insert_one(data)
    # tweetsCollection.insert_one(data2)
    ###########
    for n in range(0,len(clubTweets)):
        data3 = {"Club Name": clubName, "Tweets": clubTweets[n], "User": followers[n]}
        tweetsUsersNew.insert_one(data3)
        create_doc(uri=currentURL, doc_data={"Club Name": clubName, "Tweets": clubTweets[n], "User": followers[n]})