# -*- coding: utf-8 -*-

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

es = ElasticSearch()
currentDataBaseTerm = "dva" # Used: elvis, club, clubs, holahola, fourK, gold, diamond, mercury, dva
currentURL = "http://localhost:9200/" + currentDataBaseTerm + "/tweets" # DO NOT USE A "/" AT THE END

# _INDEX_NAME = "club"
# _USER_DOC_TYPE = 'tweet'
#
# def get_user_mapping():
#     return {
#         _USER_DOC_TYPE : {
#           'properties' : {
#               'Tweets' : {
#                   'type' : 'string',
#                   'store' : 'no',
#                   'index_options' : 'freqs',
#                   'omit_norms' : 'true',
#                   'analyzer' : 'whitespace_tokenizer'
#               },
#               'Club Name' : { 'type' : 'string' }
#           }
#       }
#   }
#
#
# def recreate_index():
#   #delete_index()
#     settings = {
#       'analysis' : {
#           'analyzer' : {
#               'whitespace_tokenizer' : {
#                   'tokenizer' : 'whitespace'
#               }
#           }
#       }
#   }
#     es.create_index(_INDEX_NAME, settings=settings)
#     es.put_mapping(_INDEX_NAME, _USER_DOC_TYPE, get_user_mapping())
#
#
# recreate_index()

consumer_key = "LsAwFJvshsac0oV1MWPT5SPdP"
consumer_secret = "HtOBG7Lv66RUIvmtffEe5LYN0RRVncuQp7p1bXoyGdNu3coYkw"

access_key = "2183673402-AvddwhaVAuB8lngOqVbtX31kQMpnTnbfhSOs7iO"
access_secret = "1Ar33ZPEeyEOs1gdn7aZLYq5tTyW4E3JyQaQBJyo4gUzf"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# tweepyCursor = tweepy.Cursor(api.user_timeline, screen_name="billgates", count=200).items()
# hola = ""
# n = 0
# for tweet in tweepyCursor:
#     hola = hola + tweet.text
#     n = n + 1
#     if n >= 200:
#         break

from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords
import string
punctuation = list(string.punctuation)
alphabet = list("qwertyuiopasdfghjklzxcvbnm")
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT', '…', "’", "I","”","“","—","‘"]

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def isanumber(a):

    bool_a = True
    try:
        bool_a = float(repr(a))
    except:
        bool_a = False

    return bool_a

import operator
from collections import Counter

cursor = tweetsCollection.find()

clubsTweetDict = {}
clubs = []
for item in cursor:
    if item["Club Name"] in clubsTweetDict:
        clubsTweetDict[item["Club Name"]] = clubsTweetDict[item["Club Name"]] + item["TweetsString"]
    else:
        clubsTweetDict[item["Club Name"]] = item["TweetsString"]
        clubs.append(item["Club Name"])

def freqCount(hola):
    count_all = Counter()
    terms_hash = [term for term in preprocess(hola) if term.startswith('#')]
    terms_users = [term for term in preprocess(hola) if term.startswith('@')]
    terms_only = [term.lower() for term in preprocess(hola) if term.lower() not in stop and not term.startswith(('#', '@', 'http')) and not isanumber(term)]
    count_all.update(terms_only)

    countList = count_all.most_common()
    # print(count_all.most_common(10))
    # countList = count_all
    saveList = []
    for i in countList:
        saveList.append(i[0])
    return saveList

termsDict = {}
termListDuplicates = []
termList = []
progressNum = 0
for club in clubs:
    # Gather the aggregated tweets for the given club and store them in holad
    holad = clubsTweetDict[club]

    # Get all the terms from all of the tweets and store them in wordsArray
    wordsArray = []
    for jonah in holad:
        for word in freqCount(hola=jonah):
            wordsArray.append(word)
            termListDuplicates.append(word)

    # Assign the list of terms to the club and store it in termDict
    termsDict[club] = wordsArray
    progressNum += 1
    print(progressNum)

# print(termsDict[clubs[0]][0])

# Duplicate free term list stored in termList
print(len(termListDuplicates))
progressNum = 0
progressPercent = 0
for word in termListDuplicates:
    if word not in termList:
        termList.append(word)
    progressNum += 1
    newProgressPercent = progressNum/len(termListDuplicates) * 100
    if newProgressPercent >= progressPercent + 0.1:
        progressPercent = newProgressPercent
        print("{}%".format(round(progressPercent, 1)))
print(len(termList))

documentFrequencies = {}
progressNum = 0
progressPercent = 0
# Go through every term and check how many clubs contain it, then store this in documentFrequencies and the documentCollection mongo DB
for word in termList:
    for club in clubs:
        if word in termsDict[club] and word in documentFrequencies:
            documentFrequencies[word] += 1
        elif word in termsDict[club]:
            documentFrequencies[word] = 1
    data = {"Term": word, "df": documentFrequencies[word]}
    documentCollection.insert_one(data)

    progressNum += 1
    newProgressPercent = progressNum/len(termList) * 100
    if newProgressPercent >= progressPercent + 0.001:
        progressPercent = newProgressPercent
        print("{}%".format(round(progressPercent, 3)))

print(documentFrequencies["the"])
print(documentFrequencies["mast"])

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
    tweepyCursor = tweepy.Cursor(api.user_timeline, screen_name=user, count=200).items()
    hola = ""
    n = 0
    for tweet in tweepyCursor:
        hola = hola + tweet.text
        n = n + 1
        if n >= 200:
            break
    userList = freqCount(hola)
    king = search(uri=currentURL + "/_search?", term=hola)

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
    termsArray = []
    allTermsArray = []
    realTermsArray = []
    tupleTermsArray = []
    for item in sortedArray:
        termsArray.append(termsDict[item])
    for term in termsArray:
        for termit in term:
            allTermsArray.append(termit)
    for word in userList:
        i = 0
        for term in allTermsArray:
            i = i + 1
            if word == term and word not in realTermsArray:
                realTermsArray.append(word)
                tupleTermsArray.append((word,i))
    tupleTermsArray.sort(key=lambda tup: tup[1])
    tupleTermsArray = tupleTermsArray[:10]
    realTermsArray = []
    for item in tupleTermsArray:
        realTermsArray.append(item[0])
    return [sortedArray, realTermsArray]

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

# cursor = tweetsCollection.find({})
# bob = []
# twitters = []
# clubsBOB = []
# for item in cursor:
#     print(item["Club Name"])
#     clubsBOB.append(item["Club Name"])
#     twitters.append(item["Twitter Account"])
#     # print(item["_id"])
#
# for num in range(0,len(twitters)):
#     addTwitterUser(user=twitters[num], clubName=clubsBOB[num])
#     bob.append(clubsBOB[num])
#     print("Done")
#     for bobs in bob:
#         print(bobs)

# cursor = tweetsUsers.find({})
# #
# for item in cursor:
#     dataToSearch = {"Tweets": item["Tweets"], "Club Name": item["Club Name"]}
#     es.index_op(dataToSearch, _USER_DOC_TYPE, True)
#     print(item["Club Name"])
#     create_doc(uri=currentURL, doc_data=dataToSearch)

#consumer_key = "LsAwFJvshsac0oV1MWPT5SPdP"
#consumer_secret = "HtOBG7Lv66RUIvmtffEe5LYN0RRVncuQp7p1bXoyGdNu3coYkw"
#
#access_key = "2183673402-AvddwhaVAuB8lngOqVbtX31kQMpnTnbfhSOs7iO"
#access_secret = "1Ar33ZPEeyEOs1gdn7aZLYq5tTyW4E3JyQaQBJyo4gUzf"
#
#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_key, access_secret)
#
#api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
#
#r8Limit = api.rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['remaining']
#print(r8Limit)
#
#cursorDB = collection.find({})
#
#fn = 0
#n = 0
#
#for item in cursorDB:
#    followers = item.get("Followers")
#    userTweetsConCat = []
#    for follower in followers:
#        tweetConCat = ""
#        test = []
#        print (follower)
#        url = "https://twitter.com/" + follower
#        try:
#            with urllib.request.urlopen(url) as url:
#                f = url.read()
#        except urllib.error.HTTPError as e:
#            print("Skipping" + follower)
#            continue
#        soup = BeautifulSoup(f, 'html.parser')
#        if soup.findAll("h2", { "class" : "ProtectedTimeline-heading" }) != [] or soup.findAll("div", {"class": "body-content"}) != [] or soup.findAll("div", {"class": "flex-module error-page clearfix"}) != []:
#            print("Skipping " + follower)
#        else:
#            try:
#                tweepyCursor = tweepy.Cursor(api.user_timeline, screen_name=follower, count=200).items()
#                for tweet in tweepyCursor:
#                    hola = tweet.text
#                    test.append(hola)
#                    if len(test) >= 200:
#                        break
#                fn = fn + 1
#                print(str(fn) + "/8474" + " (" + str(fn/8474*100) + "%)" " Users Processed")
#            except tweepy.error.TweepError as e:
#                print("Exception")
#                time.sleep(60*15)
#                print("Out-waited exception")
#                tweepyCursor = tweepy.Cursor(api.user_timeline, screen_name=follower, count=200).items()
#                for tweet in tweepyCursor:
#                    hola = tweet.text
#                    test.append(hola)
#                    if len(test) >= 200:
#                        break
#                fn = fn + 1
#                print(str(fn) + "/6528" + " (" + str(fn/6528*100) + "%)" " Users Processed")
#            for testObject in test:
#                tweetConCat = tweetConCat + testObject
#            userTweetsConCat.append(tweetConCat)
#    data = {"Club Name": item.get("Club Name"), "Twitter Account": item.get("Twitter Account"), "Followers": followers, "TweetsString": userTweetsConCat}
#    tweetsCollection.insert_one(data)
#    n = n + 1
#    print("\n" + str(n) + " Clubs Processed" + "\n")

#time.sleep(60*15)

#print api.rate_limit_status()['resources']['followers']['/followers/list']['remaining']

#i = 0
#for n in range(0, len(clubNames)):
#    if twitterAccounts[n] != "No Results":
##        f = api.rate_limit_status()['resources']['followers']['/followers/list']['remaining']
#        tweepyCursor = tweepy.Cursor(api.followers, screen_name=twitterAccounts[n], count=200).items()
#        currentFollowers = []
#        if i >= 14:
#            print "Waiting"
#            time.sleep(60 * 15)
#            print "Done Waiting"
#            i = 0
#        for follower in tweepyCursor:
#            if i >= 14:
#                print "Waiting"
#                time.sleep(60 * 15)
#                print "Done Waiting"
#                i = 0
#            currentFollowers.append(follower.screen_name)
#            if len(currentFollowers) >= 200:
#                break
#        data = {"Club Name": clubNames[n], "Twitter Account": twitterAccounts[n], "Followers": currentFollowers}
#        i = i + 1
#        print data
#        collection.insert_one(data)
#        print str(n) + " Clubs Processed"
#    else:
#        continue

#collection_id = collection.insert(data)
#print collection_id

#print collection.find_one({"hola": "hello"})

#class MyStreamListener(tweepy.StreamListener):
#
#    def on_status(self, status):
#        print(status.text.encode('ascii', 'ignore') + '\n')
#
#    def on_error(self, status_code):
#        if status_code == 420:
#            #returning False in on_data disconnects the stream
#            return False

#def main():
#    #Perform OAuth 3-handshake dance:
#    consumer_key = "LsAwFJvshsac0oV1MWPT5SPdP"
#    consumer_secret = "HtOBG7Lv66RUIvmtffEe5LYN0RRVncuQp7p1bXoyGdNu3coYkw"
#
#    access_key = "2183673402-AvddwhaVAuB8lngOqVbtX31kQMpnTnbfhSOs7iO"
#    access_secret = "1Ar33ZPEeyEOs1gdn7aZLYq5tTyW4E3JyQaQBJyo4gUzf"
#
#    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#    auth.set_access_token(access_key, access_secret)
#
#    api = tweepy.API(auth)
#
#    tweepyCursor = tweepy.Cursor(api.followers, screen_name="@1835Hinman").items()
#
#    while True:
#        try:
#            for user in tweepyCursor:
#                print user.screen_name
#        except tweepy.TweepError:
#            time.sleep(60 * 15)
#            continue
#        except StopIteration:
#            break

#   myStreamListener = MyStreamListener()
#   myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
#   myStream.filter(locations=[-87.683380,42.048625,-87.666849,42.063387])

#   Return auth'd api instance for SearchUser()
#   return api,auth

#if __name__=='__main__':
#    main()


#import urllib
#from bs4 import BeautifulSoup
#
#text_file = open("readableList.txt", "r")
#lines = text_file.read().split('\n')
#text_file.close()
#
#clubsWithTwitter = 0
#clubsWithoutTwitter = 0
#
#text_file = open("foundTwitter.txt", "w")
# other_text_file = open("twitterName.txt", "w")
#
# privateAccounts = []
#
# cursorDB = collection.find({})
#
# n = 0
#
# for item in cursorDB:
#    followers = item.get("Followers")
#    for follower in followers:
#        url = "https://twitter.com/" + follower
#        f = urllib.urlopen(url)
#
#        soup = BeautifulSoup(f, 'html.parser')
#
#        if soup.findAll("h2", { "class" : "ProtectedTimeline-heading" }) != []:
#            privateAccounts.append(follower)
#            print "\n"+ follower + " PRIVATE" + "\n"
#        elif soup.findAll("div", {"class": "body-content"}) != []:
#            privateAccounts.append(follower)
#            print "\n" + follower + " DOES NOT EXIST" + "\n"
#        else:
#            print follower + " Cleared"
#    n = n + 1
#    print str(n) + " Clubs Processed"
#
# print privateAccounts
#
# for club in lines:
#    input = club.replace(" ", "%20")
#
#    url = "https://twitter.com/search?f=users&vertical=default&q="+input+"&src=typd"
#    f = urllib.urlopen(url)
#
#    soup = BeautifulSoup(f, 'html.parser')
#
#    if soup.findAll("a", { "class" : "ProfileNameTruncated-link u-textInheritColor js-nav js-action-profile-name" }) == []:
#        print "No Results"
#        text_file.write("No Results\n")
#        other_text_file.write("{} - No Results\n".format(club))
#        clubsWithoutTwitter += 1
#    else:
#        links = soup.findAll("a", { "class" : "ProfileNameTruncated-link u-textInheritColor js-nav js-action-profile-name" })
#        twitterAccount = links[0].get('href').replace("/", "@")
#        print twitterAccount
#        text_file.write(twitterAccount + "\n")
#        other_text_file.write(club + " - " + twitterAccount + "\n")
#        clubsWithTwitter +=1
#
#print "{} Clubs with Twitter\n{} Clubs without Twitter".format(clubsWithTwitter, clubsWithoutTwitter)
#text_file.close()
#other_text_file.close()

#398 Clubs with Twitter
#182 Clubs with out Twitter
#598 Total Clubs
