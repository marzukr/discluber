from collections import Counter

import re
from nltk.corpus import stopwords
import string

import emoji

from enum import Enum

from math import log

class Token(Enum):
    TERM = "Terms"
    HASHTAG = "Hashtags"
    USER = "Users"
    LINK = "Links"

# Define constants to filter and sort terms in Twitter strings
punctuation = list(string.punctuation)
alphabet = list("qwertyuiopasdfghjklzxcvbnm")
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT', '…', "’", "I","”","“","—","‘"]
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

#Get all individual elements (tokens) from tweets
def preprocess(s, lowercase=False):
    tokens = tokens_re.findall(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def isanumber(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

# Returns complete list of terms (possibly more than one of each term) in a given aggregation of tweets
def termList(preprocessedTweets):
    #Word terms (not in stoplist, not a hastag, not a user, not a link, not a number, not an emoticon and not an emoji)
    terms_only = [
        term.lower() for term in preprocessedTweets if term.lower() 
        not in stop and 
        not term.startswith(('#', '@', 'http')) and 
        not isanumber(term) and
        not emoticon_re.match(term) and
        not term[0] in emoji.UNICODE_EMOJI
    ]
    return terms_only

# Returns complete list of hashtags (possibly more than one of each hashtag) in a given aggregation of tweets
def hashtagList(preprocessedTweets):
    terms_hash = [term for term in preprocessedTweets if term.startswith('#') and term != "#"]
    return terms_hash

# Returns complete list of users (possibly more than one of each user) in a given aggregation of tweets
def userList(preprocessedTweets):
    terms_users = [term for term in preprocessedTweets if term.startswith('@') and term != "@"]
    return terms_users

# Returns complete list of links (possibly more than one of each link) in a given aggregation of tweets
def linkList(preprocessedTweets):
    term_links = [term for term in preprocessedTweets if term.startswith('http') and term != "http"]
    return term_links

# Returns the frequencies of the specfied tokens in the given tweet aggregation
def freqCount(userTweets, token=Token.TERM):
    preprocessedTweets = preprocess(userTweets)
    filteredTweets = []
    if token == Token.TERM:
        filteredTweets = termList(preprocessedTweets)
    elif token == Token.HASHTAG:
        filteredTweets = hashtagList(preprocessedTweets)
    elif token == Token.USER:
        filteredTweets = userList(preprocessedTweets)
    elif token == Token.LINK:
        filteredTweets = linkList(preprocessedTweets)

    count_all = Counter()
    count_all.update(filteredTweets)
    return count_all

# Returns a list of tokens using the tf-idf algorithm on the given tweet aggregation
def tokenList(userTweets, tokenType, maxItems, mongoCollection):
    listWithCounts = freqCount(userTweets, tokenType)
    totalTermCount = sum(listWithCounts.values())
    tfidfArray = [] # Array of tuples -> (term, tfidfScore)
    for tokenItem in mongoCollection.find({"Term": {"$in": list(listWithCounts.keys())}}):
        term = tokenItem["Term"]
        documentFreq = listWithCounts[term]
        tf = documentFreq/totalTermCount
        df = 50/tokenItem["df"]
        tfidfCalc = tf * log(df)
        tfidfArray.append((term, tfidfCalc))
    tfidfArray.sort(key=lambda tup: tup[1], reverse=True) #Sort from highest tfidf score to lowest
    if len(tfidfArray) > maxItems: #Only return up to maxItems terms
        tfidfArray = tfidfArray[:maxItems]
    return tfidfArray

# Format the results outputted by tokenList
def formatResults(tfidfResults, tokenType):
    tokenObject = {"name": tokenType.value}
    tokenList = []
    for token in tfidfResults:
        tokenURL = "https://twitter.com/search?q=" + token[0]
        tokenURLObject = {"text": token[0], "url": tokenURL, "tfidfScore": token[1]}
        tokenList.append(tokenURLObject)
    tokenObject["list"] = tokenList
    # Format
    # {
    #     "name": "Terms", 
    #     "list": [
    #         {
    #             "text": "test", 
    #             "url": "test.com", 
    #             "tfidfScore": "0.3"
    #         },
    #         ...
    #     ]
    # }
    return tokenObject

# Return formatted results for a list of token types
def tokenResults(userTweets, tokenTypes, maxItems, mongoCollection):
    #Get a list of unformatted result lists
    unformattedResults = {}
    for tokenType in tokenTypes:
        unformatTokens = tokenList(userTweets, tokenType, maxItems, mongoCollection)
        unformattedResults[tokenType] = unformatTokens
    
    #Format the unformatted results and store them in a list
    formattedResults = []
    for tokenType, unformatTokens in unformattedResults.items():
        formattedObject = formatResults(unformatTokens, tokenType)
        formattedResults.append(formattedObject)
        
    # Format
    # [
    #     {
    #         "name": "Terms", 
    #         "list": [
    #             {
    #                 "text": "test", 
    #                 "url": "test.com", 
    #                 "tfidfScore": "0.3"
    #             },
    #             ...
    #         ]
    #     },
    #     ...
    # ]
    
    return formattedResults
