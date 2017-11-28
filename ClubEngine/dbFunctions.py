import tfidfEngine
from tqdm import tqdm
from collections import Counter

def clubTweetTokens(tweetCollection, returnLength=False):
    length = 0
    clubItemIDS = [clubItem["_id"] for clubItem in tweetCollection.find({})]
    for clubItemID in clubItemIDS:
        clubItem = tweetCollection.find_one({"_id": clubItemID})
        tokens = []
        for tweetAgg in clubItem["TweetsString"]:
            tokens += tfidfEngine.preprocess(tweetAgg, True)
        uTokens = list(set(tokens))
        if returnLength:
            length += len(uTokens)
        else:
            for uToken in uTokens:
                yield uToken
    if returnLength:
        yield length

def storeDocumentFreq(freqCollection, tweetCollection):
    # totalTokens = next(clubTweetTokens(tweetCollection, returnLength=True))
    totalTokens = 2500000
    pbar = tqdm(total=totalTokens)
    tokenCounter = Counter()
    for token in clubTweetTokens(tweetCollection):
        # freqCollection.update_one({"Term": token}, {"$inc": {"df": 1}}, upsert=True)
        # freqCollection.insert_one({"Term": token})
        tokenCounter.update([token])
        pbar.update(1)
    pbar.close()

    pbar = tqdm(total=len(tokenCounter))
    for token, freq in tokenCounter.items():
        freqCollection.insert_one({"Term": token, "df": freq})
        pbar.update(1)
    pbar.close()

def runFunction(freqCollection, tweetCollection):
    storeDocumentFreq(freqCollection, tweetCollection)
