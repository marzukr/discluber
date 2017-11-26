from collections import Counter

import re
from nltk.corpus import stopwords
import string

import emoji

from enum import Enum, auto

class Token(Enum):
    TERM = auto()
    HASHTAG = auto()
    USER = auto()
    LINK = auto()

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
    terms_hash = [term for term in preprocessedTweets if term.startswith('#')]
    return terms_hash

# Returns complete list of users (possibly more than one of each user) in a given aggregation of tweets
def userList(preprocessedTweets):
    terms_users = [term for term in preprocessedTweets if term.startswith('@')]
    return terms_users

# Returns complete list of links (possibly more than one of each link) in a given aggregation of tweets
def linkList(preprocessedTweets):
    term_links = [term for term in preprocessedTweets if term.startswith('http')]
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
        filteredTweets = userList(preprocessedTweets)

    count_all = Counter()
    count_all.update(filteredTweets)
    return count_all