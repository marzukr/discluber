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

# cursor = tweetsCollection.find()
#
# clubsTweetDict = {}
# clubs = []
# for item in cursor:
#     if item["Club Name"] in clubsTweetDict:
#         clubsTweetDict[item["Club Name"]] = clubsTweetDict[item["Club Name"]] + item["TweetsString"]
#     else:
#         clubsTweetDict[item["Club Name"]] = item["TweetsString"]
#         clubs.append(item["Club Name"])

# tfidf = 440000
# import random
# def t2CC():
#     t2calc = random.randint(0,200000)
#     return t2calc
# def tfidf():
#     tfidf = random.randint(300000,440000)
#     return tfidf

# termsDict = {}
# termListDuplicates = []
# termList = []
# progressNum = 0
# for club in clubs:
#     # Gather the aggregated tweets for the given club and store them in holad
#     holad = clubsTweetDict[club]
#
#     # Get all the terms from all of the tweets and store them in wordsArray
#     wordsArray = []
#     for jonah in holad:
#         for word in freqCount(hola=jonah):
#             wordsArray.append(word)
#             termListDuplicates.append(word)
#
#     # Assign the list of terms to the club and store it in termDict
#     termsDict[club] = wordsArray
#     progressNum += 1
#     print(progressNum)
#
# # print(termsDict[clubs[0]][0])
#
# # Duplicate free term list stored in termList
# print(len(termListDuplicates))
# progressNum = 0
# progressPercent = 0
# for word in termListDuplicates:
#     if word not in termList:
#         termList.append(word)
#     progressNum += 1
#     newProgressPercent = progressNum/len(termListDuplicates) * 100
#     if newProgressPercent >= progressPercent + 0.1:
#         progressPercent = newProgressPercent
#         print("{}%".format(round(progressPercent, 1)))
# print(len(termList))
#
# documentFrequencies = {}
# progressNum = 0
# progressPercent = 0
# # Go through every term and check how many clubs contain it, then store this in documentFrequencies and the documentCollection mongo DB
# for word in termList:
#     for club in clubs:
#         if word in termsDict[club] and word in documentFrequencies:
#             documentFrequencies[word] += 1
#         elif word in termsDict[club]:
#             documentFrequencies[word] = 1
#     data = {"Term": word, "df": documentFrequencies[word]}
#     documentCollection.insert_one(data)
#
#     progressNum += 1
#     newProgressPercent = progressNum/len(termList) * 100
#     if newProgressPercent >= progressPercent + 0.001:
#         progressPercent = newProgressPercent
#         print("{}%".format(round(progressPercent, 3)))
#
# print(documentFrequencies["the"])
# print(documentFrequencies["mast"])
# import locale
# locale.setlocale(locale.LC_ALL, 'en_US')
# previousOnes = {}
#
# while 0==0:
#     term = input("Term: ")
#     if term not in previousOnes:
#         result = documentCollection.find_one({'Term': term})
#         if result is not None:
#             dfCalc = result["df"]*tfidf() + t2CC()
#             print(locale.format("%d", dfCalc, grouping=True))
#             previousOnes[term] = dfCalc
#         else:
#             print("No results")
#     else:
#         dfCalc = previousOnes[term]
#         print(locale.format("%d", dfCalc, grouping=True))

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
