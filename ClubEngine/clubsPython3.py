# -*- coding: utf-8 -*-

# from ClubEngine import tfidfEngine, dbFunctions
import tfidfEngine, dbFunctions

from pymongo import MongoClient
client = MongoClient()
db = client.clubsDatabase
collection = db.followersList
tweetsCollection = db.tweetsList
tweetsUsers = db.tweetsUsers
tweetsUsersNew = db.tweetsUsersNew

# documentCollection = db.documentCollection
documentCollection = db.testFreqs

# from elasticsearch import Elasticsearch, exceptions
from pyelasticsearch import ElasticSearch
import requests
import json
import tweepy

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
    #Take the term and run it through elasticsearch

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

def format_results(results, ouputParam):
    #Takes elasticsearch output and makes it into a list of clubs, some of which repeat
    #LOOK INTO THIS TO OPTIMIZE RESULTS

    data = [doc for doc in results['hits']['hits']]
    prettyA = []
    for doc in data:
        # CHANGE THIS for different outputs
        pretty = "%s" % (doc['_source'][ouputParam])
        prettyA.append(pretty)
    return prettyA

def create_doc(uri, doc_data):
    """Create new document."""
    query = json.dumps(doc_data)
    response = requests.post(uri, data=query)
    print(response)

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

    #Take the combined tweet string and feed it into elastic search, then make the result into a pretty list of clubs
    rawElasticSearchResults = search(uri=currentURL + "/_search?", term=userTweets)
    clubsArray = format_results(results=rawElasticSearchResults, ouputParam="Club Name")

    points = []
    uPoints = []
    uniqueClubs = []
    #Assign points such that the clubs that come first have more
    for n in range(0,len(clubsArray)):
        points.append(len(clubsArray) - n)

    #Get a list of unique clubs
    for club in clubsArray:
        if club not in uniqueClubs:
            uniqueClubs.append(club)

    #Add the points of duplicate clubs together so that each unique club has only one point value
    for uClub in uniqueClubs:
        for cClub in clubsArray:
            if cClub == uClub:
                uIndex = uniqueClubs.index(uClub)
                cindex = clubsArray.index(cClub)
                if 0 <= uIndex < len(uPoints):
                    uPoints[uIndex] = uPoints[uIndex] + points[cindex]
                else:
                    uPoints.append(points[cindex])

    #Sort the list of unique clubs by the point value so that the highest points are first
    sortedArray = [x for (y, x) in sorted(zip(uPoints, uniqueClubs), reverse=True)][0:3]

    #Get the profile image URLS for the clubs and reorganize the data
    clubData = []
    for club in sortedArray:
        clubHandle = collection.find_one({"Club Name": club})["Twitter Account"]
        clubImageURL = api.get_user(clubHandle).profile_image_url_https.replace("_normal", "_200x200")
        newClubDataObject = {"name": club, "handle": clubHandle, "imageURL": clubImageURL}
        clubData.append(newClubDataObject)

    #Get results from the TFIDF engine
    formattedTerms = tfidfEngine.tokenResults(userTweets, [tfidfEngine.Token.TERM], 10, documentCollection)
    
    return {"clubs": clubData, "terms": formattedTerms}

# ----> LEGACY CODE BELOW THIS POINT <----

# LEGACY CODE UNKNOWN FUNCTION
# def newIndex():
#     cursor = tweetsUsers.find({})
#     for item in cursor:
#         dataToSearch = {"Tweets": item["Tweets"], "Club Name": item["Club Name"]}
#         print(item["Club Name"])
#         create_doc(uri=currentURL, doc_data=dataToSearch)

# LEGACY CODE TO UPDATE/ADD TO DATABASE
# def addTwitterUser(user, clubName):
#     followersCursor = tweepy.Cursor(api.followers, screen_name=user, count=300).items()
#     fabio = []
#     for fob in followersCursor:
#         fabio.append(fob.screen_name)
#         if len(fabio) >= 200:
#             break
#     followers = []
#     clubTweets = []
#     for followerH in fabio:
#         follower = followerH
#         url = "https://twitter.com/%s" % follower
#         tweetConCat = ""
#         tweetsA = []
#         try:
#             with urllib.request.urlopen(url) as url:
#                 f = url.read()
#         #urllib.error.HTTPError as e
#         except:
#             print("Skipping(1) " + follower)
#             continue
#         soup = BeautifulSoup(f, 'html.parser')
#         def do_it():
#             print("Adding %s Tweets" % follower)
#             tweepyCursor = tweepy.Cursor(api.user_timeline, screen_name=follower, count=200).items()
#             for tweet in tweepyCursor:
#                 hola = tweet.text
#                 tweetsA.append(hola)
#                 if len(tweetsA) >= 200:
#                     break
#         if soup.findAll("h2", { "class" : "ProtectedTimeline-heading" }) != [] or soup.findAll("div", {"class": "body-content"}) != [] or soup.findAll("div", {"class": "flex-module error-page clearfix"}) != []:
#             print("Skipping(2) " + follower)
#             continue
#         else:
#             try:
#                 do_it()
#             except tweepy.error.TweepError as e:
#                 print("Exception")
#                 time.sleep(60*15)
#                 print("Out-waited exception")
#                 do_it()
#             for objectT in tweetsA:
#                 tweetConCat = tweetConCat + objectT
#         followers.append(follower)
#         clubTweets.append(tweetConCat)
#         if len(followers) >= 200:
#             break
#     data = {"Club Name": clubName, "Twitter Account": user, "Followers": followers}
#     data2 = {"Club Name": clubName, "Twitter Account": user, "Followers": followers, "TweetsString": clubTweets}
#     # RE ENABLE FOR REGULAR USE #
#     # collection.insert_one(data)
#     # tweetsCollection.insert_one(data2)
#     ###########
#     for n in range(0,len(clubTweets)):
#         data3 = {"Club Name": clubName, "Tweets": clubTweets[n], "User": followers[n]}
#         tweetsUsersNew.insert_one(data3)
#         create_doc(uri=currentURL, doc_data={"Club Name": clubName, "Tweets": clubTweets[n], "User": followers[n]})
