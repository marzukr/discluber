import tfidfEngine, twitterUtil, config, clubsPython3

from collections import Counter

def clubAvgResults(club, collection):
    occurences = []
    for entry in config.dbCol(collection).find({"twitterAccount": club}):
        occurences += entry["results"]
    counts = Counter(occurences).most_common(10)
    print(counts)
    print(len(occurences))
    
clubAvgResults("thedailynu", "validation3")