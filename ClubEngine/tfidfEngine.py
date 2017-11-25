import operator
from collections import Counter

from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords
import string

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

# def isanumber(a):
#     bool_a = True
#     try:
#         bool_a = float(repr(a))
#     except:
#         bool_a = False

#     return bool_a

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
 

# Returns the terms in a given aggregation of tweets
def freqCount(userTweets, shouldReturnListOnly):
    count_all = Counter()

    preprocessedTweets = preprocess(userTweets)
    terms_hash = [term for term in preprocessedTweets if term.startswith('#')]
    terms_users = [term for term in preprocessedTweets if term.startswith('@')]
    term_links = [term for term in preprocessedTweets if term.startswith('http')]

    #Word terms (not in stoplist, not a hastag, not a user, not a link, not a number, and not an emoticon and/or emoji)
    terms_only = [
        term.lower() for term in preprocessedTweets if term.lower() 
        not in stop and 
        not term.startswith(('#', '@', 'http')) and 
        not isanumber(term) and
        not emoticon_re.match(term)
    ]

    count_all.update(terms_only)
    print(count_all)

    #Array of the most common terms with usage numbers [(String, usage),]
    countList = count_all.most_common(10)
    # print(count_all.most_common(10))
    # countList = count_all

    #Whether or not to return the terms and list, or just terms
    if shouldReturnListOnly:
        saveList = []
        for i in countList:
            saveList.append(i[0])
        return saveList
    else:
        return countList
