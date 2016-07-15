# -*- coding: utf-8 -*-

import pymongo
#import tweepy
#import time
#import sys
#import bson
#import urllib.request
#from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient()
db = client.clubsDatabase
collection = db.followersList
tweetsCollection = db.tweetsList

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
#other_text_file = open("twitterName.txt", "w")
#
#privateAccounts = []
#
#cursorDB = collection.find({})
#
#n = 0
#
#for item in cursorDB:
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
#print privateAccounts

#for club in lines:
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
#182 Clubs without Twitter
#598 Total Clubs
