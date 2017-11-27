clubsOrganizations README
============
An online tool to recommend a club to a given NU student based on their tweets.

## Mongo Databases
The database is called "clubsDatabase"

**followersList**
+ "Twitter Account": The twitter username of the club (with "@" prefix)
+ "Club Name": The readable string name of the club.
+ "Followers": An array of the username of up to 200 followers of the club (no "@" prefix)

**tweetsList**
+ "Twitter Account": The twitter username of the club (with "@" prefix)
+ "Club Name": The readable string name of the club.
+ "Followers": An array of the username of up to 200 followers of the club (no "@" prefix)
+ "Tweets String": An array of up to 200 tweets of each follower concatenated into one string.

**tweetsUsers**
+ "Club Name": The readable string name of the club. (Same as "tweetsList" collection)
+ "Tweets": "Tweets String" array of "tweetsList" collection concatenated into one list

**tweetsUsersNew**
+ "Club Name": The readable string name of the club. (Same as "tweetsUsers" collection)
+ "Tweets": Same as "Tweets" property of "tweetsUsers" collection
+ "User": The twitter follower of the club that the "Tweets" were pulled from (no "@" prefix)

**documentCollection**
+ "Term": A term that was used the tweets of a follower of a club
+ "df": How many clubs that term appeared in
