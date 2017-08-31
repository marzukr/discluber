from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords
import string
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

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def isanumber(a):
    bool_a = True
    try:
        bool_a = float(repr(a))
    except:
        bool_a = False

    return bool_a

import operator
from collections import Counter

def freqCount(userTweets, shouldReturnListOnly):
    count_all = Counter()
    terms_hash = [term for term in preprocess(userTweets) if term.startswith('#')]
    terms_users = [term for term in preprocess(userTweets) if term.startswith('@')]
    terms_only = [term.lower() for term in preprocess(userTweets) if term.lower() not in stop and not term.startswith(('#', '@', 'http')) and not isanumber(term)]
    count_all.update(terms_only)

    countList = count_all.most_common()
    # print(count_all.most_common(10))
    # countList = count_all
    saveList = []
    if shouldReturnListOnly:
        for i in countList:
            saveList.append(i[0])
        return saveList
    else:
        return countList
