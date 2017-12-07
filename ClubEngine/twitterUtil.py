import tweepy
from ClubEngine import dbFunctions

consumer_key = dbFunctions.getConfig("consumerKey")
consumer_secret = dbFunctions.getConfig("consumerSecret")
access_key = dbFunctions.getConfig("accessKey")
access_secret = dbFunctions.getConfig("accessSecret")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
twitterAPI = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def getFollowers(twitterAccount):
    followersPages = tweepy.Cursor(twitterAPI.followers, screen_name=twitterAccount).items()
    followersTwitters = (user.screen_name for i, user in enumerate(followersPages))
    return followersTwitters

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

# def getFollowerTweets(twitterAccount):
#     followerTweets = {}
