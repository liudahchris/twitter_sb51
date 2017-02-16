from collections import defaultdict
import pymongo
from clean_date import _bin_date
import numpy as np
import string
from nltk.corpus import stopwords

def clean_text(tweet,stopwords,punc):
    '''
    Takes a tweet, lowers and strips punctuation, and removes stopwords and tags
    INPUT: string
    OUTPUT: string
    '''
    # Lowercase, strip punctation, tokenize
    tokens = tweet.lower().translate(None,punc).split()
    # Remove stopwords and hashtags
    tokens = [token for token in tokens if token[0]!='#' and token not in stopwords]
    return ' '.join(tokens)

def dict_to_csv(d,outname,key_names='col1',val_names='col2'):
    '''
    Writes dictionary key and value pairs into CSV file.
    INPUT: dict, str, str(optional), str(optional)
    OUTPUT: None
    '''
    with open(outname,'w') as f:
        f.write('{},{}\n'.format(key_names,val_names))
        for key in sorted(d):
            f.write('{}, {}\n'.format(key,d[key]))
    return None


def aggregate_tweets(src_coll,target_coll,verbose=False):
    '''
    Takes a source collection and aggregates it into new collection.
    Source collection docs have structure:
        - created_at
        - text
    Target collection has structure:
        - time
        - tweets (array of tweets)
    INPUT: source pymongo collection, target pymongo collection, bool
    OUTPUT: None
    '''
    START_TIME = "2017/02/05 22:30:00"
    END_TIME = "2017/02/06 04:30:00"
    STOPWORDS = stopwords.words('english')

    # Punctuation to remove
    # We'll keep @ to look at popular users and # to filter out hashtags
    PUNC = string.punctuation.translate(None,'@#')

    for i,tweet in enumerate(src_coll.find()):
        print_status(i,verbose=verbose)
        # Bin time
        time = _bin_date(tweet['created_at'],bin_size=60)
        if time < START_TIME or time > END_TIME:
            continue
        text = clean_text(tweet['text'],stopwords=STOPWORDS,punc=PUNC)
        # Add tweet text to time slot
        target_coll.update_one({'time':time},{'$push':{'tweets':text}},upsert=True)
    return None

def count_tweets(coll):
    '''
    Function takes in pymongo collection containing fields:
        - time (string in form %Y/%m/%d %H:%M:%S)
        - tweets (arr)
    Iterates and adds field "counts", corresponding to number of tweets at time
    INPUT: pymongo collection object
    OUTPUT: None
    '''
    for doc in coll.find():
        time = doc['time']
        count = len(doc['tweets'])
        coll.update_one({'time':time},{'$set':{'count':count}})
    return None

def print_status(i,n=10000,verbose=True):
    '''
    Prints statement after ever n tweets are processed
    '''
    if verbose and i%n==0:
        print "{} tweets processed".format(i)
    return


def main():
    '''
    This script will take clean data and do a raw count and word count.
    The Super Bowl started about approx. Feb 05 2017 3:30pm pst
    and ended at about Feb 05 2017 7:30pm pst.
    These translate to Feb 05 22:30:00 UTC and Feb 06 4:30:00 UTC.
    The dates should be clean (from clean_tweets.py), so comparisons
    should make sense.

    We'll store this data in another collection in Mongo to
    '''
    client = pymongo.MongoClient()
    db = client['clean_tweets']
    coll = db['clean_tweets']
    target = db['binned_tweets']

    VERBOSE = True

    # Build new collection that has fields time and tweets during that time
    print 'Aggregating tweets...'
    aggregate_tweets(coll,target,VERBOSE)
    # Takes newly generated collection and adds field 'count' to it
    print 'Counting tweets...'
    count_tweets(target)

    client.close()
    return None


if __name__=='__main__':
    main()
