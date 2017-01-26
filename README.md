clubsOrganizations README
============
An online tool to recommend a club to a given NU student based on their tweets.

## Mongo Databases
All Mongo databases contain "{underscore}_id" (remove {underscore}) as a key

**followersList**
+ A list of all the followers for a club
+ ["Followers", "Twitter Account", "Club Name"]

**tweetsList**
+ A list of all the tweets together for a given club.
+ ["Twitter Account", "Club Name", "Followers", "Tweets String"]

**tweetsUsers**
+ Individual Tweets sorted by clubName
+ ["Tweets", "Club Name"]

**tweetsUsersNew**
+ Individual tweets sorted by user and club name
+ ["Tweets", "Club Name", "User"]

**documentCollection**
+ Terms used in all the tweets with document frequency based on each club.
+ ["Term", "df"]
