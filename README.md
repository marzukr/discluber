clubsOrganizations README
============
An online tool to recommend a club to a given NU student based on their tweets.

## Mongo Databases
The database is called "clubsDatabase"

**config**
+ "followersPerClub": How many followers to retreive per club
+ "tweetsPerFollower": How many tweets per follower to retrieve
+ "clubs": A dictionary, keys are club twitter handle, values are club names
+ "tweetsPerUser": The number of tweets to retreive when a user enters a twitter into Discluber
+ "clubsToReturn": The number of clubs to return when using Discluber
+ "tokensToReturn": The number of tokens to return when using Discluber
+ "coDate": The suffix to add to the collection names to get the correct collection

**clubData**
+ "twitterAccount": The twitter username of the club (no "@" prefix)
+ "clubName": The readable string name of the club.
+ "tweets": An array of concatenated follower tweets.
+ "followers": An array of the usernames of the followers of the club (no "@" prefix)
+ "followersTweets": A dictionary, keys are followers (no "@" prefix), values are their concatenated tweets
+ "testers": An array of usernames of up to 100 followers of the club not in the "followers" list

**followerData**
+ "clubName": The readable string name of the club. (Same as "clubData" collection)
+ "twitterAccount": The twitter account of the club. (Same as "clubData" collection)
+ "tweets": Concatenated tweets of the follower.
+ "follower": The twitter username (no "@" prefix) of follower that the "tweets" were pulled from.

**tokens**
+ "Term": A term that was used the tweets of a follower of a club
+ "df": How many clubs that term appeared in

**[DEPRECATED] followersList**
+ "Twitter Account": The twitter username of the club (with "@" prefix)
+ "Club Name": The readable string name of the club.
+ "Followers": An array of the username of up to 200 followers of the club (no "@" prefix)

**[DEPRECATED] tweetsList**
+ "Twitter Account": The twitter username of the club (with "@" prefix)
+ "Club Name": The readable string name of the club.
+ "Followers": An array of the username of up to 200 followers of the club (no "@" prefix)
+ "Tweets String": An array of up to 200 tweets of each follower concatenated into one string.

**[DEPRECATED] tweetsUsers**
+ "Club Name": The readable string name of the club. (Same as "tweetsList" collection)
+ "Tweets": "Tweets String" array of "tweetsList" collection concatenated into one list

**[DEPRECATED] tweetsUsersNew**
+ "Club Name": The readable string name of the club. (Same as "tweetsUsers" collection)
+ "Tweets": Same as "Tweets" property of "tweetsUsers" collection
+ "User": The twitter follower of the club that the "Tweets" were pulled from (no "@" prefix)
