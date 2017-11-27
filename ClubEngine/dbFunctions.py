import tfidfEngine

def clubTweetTokens(tweetCollection):
    count = 0
    total = tweetCollection.count()
    for clubItem in tweetCollection.find({}):
        tokens = []
        for tweetAgg in clubItem["TweetsString"]:
            tokens += tfidfEngine.preprocess(tweetAgg, True)
        uTokens = list(set(tokens))
        for uToken in uTokens:
            yield uToken

        count += 1
        progbar(count, total, 40, "Processing: " + clubItem["Club Name"])

def storeDocumentFreq(freqCollection, tweetCollection):
    for token in clubTweetTokens(tweetCollection):
        freqCollection.update_one({"Term": token}, {"$inc": {"df": 1}}, upsert=True)

def runFunction(freqCollection, tweetCollection):
    storeDocumentFreq(freqCollection, tweetCollection)
    # for i in clubTweetTokens(tweetCollection):
    #     nothing = None

def progbar(curr, total, full_progbar, status=""):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\033[K' + "\t" + '#'*filled_progbar + '-'*(full_progbar-filled_progbar) + "[{0:.2f}%]".format(frac*100) + " " + status, end='\r')
    if curr == total:
        print('\033[K')
