import tfidfEngine

from timeit import default_timer as timer

def clubTweetTokens(mongoCollection):
    for clubItem in mongoCollection.find({}):
        tokens = []
        for tweetAgg in clubItem["TweetsString"]:
            tokens += tfidfEngine.preprocess(tweetAgg, True)
        uTokens = list(set(tokens))
        for uToken in uTokens:
            yield uToken

def runFunction(mongoCollection):
    start = timer()
    generator = clubTweetTokens(mongoCollection)
    # print(next(generator))
    count = 0
    for i in generator:
        # print(next(generator))
        count += 1
    print(count)
    end = timer() 
    print("Time taken:", end - start)