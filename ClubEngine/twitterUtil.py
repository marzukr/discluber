import tweepy

def getFollowers(twitterAccount, twitterAPI):
    followersPages = tweepy.Cursor(twitterAPI.followers, screen_name=twitterAccount).items()
    followersTwitters = (user.screen_name for i, user in enumerate(followersPages))
    return followersTwitters

#There appears to be a significant delay between some iterations of the cursor, faster internet could help?
def getTweets(twitterAccount, maxTweets, twitterAPI):
    try:
        tweetCursor = tweepy.Cursor(twitterAPI.user_timeline, screen_name=twitterAccount).items(limit=maxTweets)
        tweets = [tweet.text for i, tweet in enumerate(tweetCursor)]
        return " ".join(tweets)
    except tweepy.error.TweepError:
        return None

def getImageURL(twitterAccount, twitterAPI):
    return twitterAPI.get_user(twitterAccount).profile_image_url_https.replace("_normal", "_200x200")