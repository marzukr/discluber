# ----> LEGACY CODE BELOW THIS POINT <----

# # LEGACY CODE UNKNOWN FUNCTION
# def newIndex():
#     cursor = tweetsUsers.find({})
#     for item in cursor:
#         dataToSearch = {"Tweets": item["Tweets"], "Club Name": item["Club Name"]}
#         print(item["Club Name"])
#         create_doc(uri=currentURL, doc_data=dataToSearch)

# # LEGACY CODE TO UPDATE/ADD TO DATABASE
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

# # LEGACY CODE FOR ELASTICSEARCH MLT QUERY
# def mlt(uri, user):
#     tweepyCursor = tweepy.Cursor(api.user_timeline, screen_name=user, count=200).items()
#     hola = ""
#     n = 0
#     for tweet in tweepyCursor:
#         hola = hola + tweet.text
#         n = n + 1
#         if n >= 200:
#             break
#     query = json.dumps({
#         "query":
#         {
#             "more_like_this" :
#             {
#                 "fields" : ["Tweets"],
#                 "like" : hola,
#                 "min_term_freq" : 1,
#                 "max_query_terms" : 12,
#                 "max_word_length" : 12
#             }
#         }
#     })
#     response = requests.get(uri, data=query)
#     print("hola")
#     results = json.loads(response.text)
#     print("bob")
#     print(results)
