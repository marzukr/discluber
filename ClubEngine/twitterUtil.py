import tweepy
# from ClubEngine import config
from . import config

from tqdm import tqdm

consumer_key = config.getConfig("consumerKey")
consumer_secret = config.getConfig("consumerSecret")
access_key = config.getConfig("accessKey")
access_secret = config.getConfig("accessSecret")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
twitterAPI = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def getFollowers(twitterAccount):
    while True:
        try:
            followersPages = tweepy.Cursor(twitterAPI.followers, screen_name=twitterAccount).items()
            # followersTwitters = (user.screen_name for user in followersPages)
            return followersPages
        except:
            pass

# # Retrieves accounts that are not part of the model for each club, tends to crash after a few accounts
# def getTestFollowers():
#     #Store all the club twitter account and follwer in an array
#     clubCollection = config.dbCol(config.Collections.CLUB_DATA)
#     finished = 0
#     clubs = []
#     for club in clubCollection.find({"testers": {"$exists": False}}):
#         clubs.append((club["twitterAccount"], club["followers"]))

#     #Loop through each club and get the test accounts
#     for club in clubs:
#         twitterAccount = club[0]
#         followers = club[1]
#         testFollowers = []
#         followersPages = None

#         #Gets the tweepy cursor, tends to lose connection, crash, so inside try/except
#         while True:
#             try:
#                 followersPages = getFollowers(twitterAccount)
#                 break
#             except:
#                 pass
        
#         #Test each follower to see if in model or is blank/protected, if not, add them to testers
#         for followerItem in followersPages:
#             testFollower = followerItem.screen_name
#             userTweets = getTweets(testFollower, 1)
#             if testFollower not in followers and userTweets is not None and userTweets != "":
#                 testFollowers.append(testFollower)
#                 if len(testFollowers) >= 100:
#                     break

#         #Add the testers into mongo
#         clubCollection.update({"twitterAccount": twitterAccount}, {"$set": {"testers": testFollowers}})
#         finished += 1
#         print(finished)

def replaceTestFollowers():
    clubCollection = config.dbCol(config.Collections.CLUB_DATA)
    validationCollection = config.dbCol(config.Collections.VALIDATION)
    for club in clubCollection.find():
        filteredTesters = []
        for tester in club["testers"]:
            if len(validationCollection.find_one({"tester": tester})["results"]) >= 3:
                filteredTesters.append(tester)
        clubCollection.update({"twitterAccount": club["twitterAccount"]}, {"$set": {"testers2": filteredTesters}})
            

#There appears to be a significant delay between some iterations of the cursor, faster internet could help?
def getTweets(twitterAccount, maxTweets):
    try:
        tweetCursor = tweepy.Cursor(twitterAPI.user_timeline, screen_name=twitterAccount).items(limit=maxTweets)
        tweets = [tweet.text for i, tweet in enumerate(tweetCursor)]
        return " ".join(tweets)
    except tweepy.error.TweepError:
        return None

def getImageURL(twitterAccount):
    try:
        return twitterAPI.get_user(twitterAccount).profile_image_url_https.replace("_normal", "_200x200")
    except tweepy.error.TweepError:
        return "https://cdn1.iconfinder.com/data/icons/modifiers-add-on-1-1/48/Sed-24-512.png"

def getFollowerTweets(twitterAccount):
    maxTweets = config.getConfig("tweetsPerFollower")
    maxFollowers = config.getConfig("followersPerClub")

    pbar = tqdm(total=maxFollowers, desc="    Adding " + twitterAccount)
    followerTweets = {}
    for followerItem in getFollowers(twitterAccount):
        follower = followerItem.screen_name
        if follower in followerTweets.keys():
            continue
        userTweets = getTweets(follower, maxTweets)
        if userTweets is not None and userTweets != "":
            followerTweets[follower] = userTweets
            pbar.update(1)
        if len(followerTweets) >= maxFollowers:
            break
    pbar.close()

    return followerTweets