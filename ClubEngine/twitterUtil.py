import tweepy
# from ClubEngine import config
import config

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

# Retrieves accounts that are not part of the model for each club, tends to crash after a few accounts
def getTestFollowers():
    clubCollection = config.dbCol(config.Collections.CLUB_DATA)
    finished = 0
    clubs = []
    for club in clubCollection.find({"testers": {"$exists": False}}):
        clubs.append((club["twitterAccount"], club["followers"]))
    for club in clubs:
        twitterAccount = club[0]
        followers = club[1]
        testFollowers = []
        followersPages = None
        while True:
            try:
                followersPages = getFollowers(twitterAccount)
                break
            except:
                pass
        for followerItem in followersPages:
            testFollower = followerItem.screen_name
            if testFollower in followers:
                continue
            else:
                testFollowers.append(testFollower)
            if len(testFollowers) >= 100:
                break
        clubCollection.update({"twitterAccount": twitterAccount}, {"$set": {"testers": testFollowers}})
        finished += 1
        print(finished)

#There appears to be a significant delay between some iterations of the cursor, faster internet could help?
def getTweets(twitterAccount, maxTweets):
    try:
        tweetCursor = tweepy.Cursor(twitterAPI.user_timeline, screen_name=twitterAccount).items(limit=maxTweets)
        tweets = [tweet.text for i, tweet in enumerate(tweetCursor)]
        return " ".join(tweets)
    except tweepy.error.TweepError:
        return None

def getImageURL(twitterAccount):
    return twitterAPI.get_user(twitterAccount).profile_image_url_https.replace("_normal", "_200x200")

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