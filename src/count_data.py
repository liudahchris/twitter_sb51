from collections import defaultdict
import pymongo
from clean_date import _bin_date


def bin_tweets(src_coll, target_coll, verbose=False):
    '''
    Takes a source collection and writes it into new collection.
    Source collection docs have structure:
        - created_at
        - text
    Target collection has structure:
        - time (binned)
        - text
    INPUT: source pymongo collection, target pymongo collection, bool
    OUTPUT: None
    '''
    START_TIME = "2017/02/05 22:30:00"
    END_TIME = "2017/02/06 04:30:00"

    for i, tweet in enumerate(src_coll.find()):
        print_status(i, verbose=verbose)
        # Bin time
        time = _bin_date(tweet['created_at'], bin_size=60)
        if time < START_TIME or time > END_TIME:
            continue
        text = tweet['text']
        # Add tweet text to time slot
        target_coll.insert_one({'text': text, 'time': time})
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
        coll.update_one({'time': time}, {'$set': {'count': count}})
    return None


def print_status(i, n=10000, verbose=True):
    '''
    Prints statement after ever n tweets are processed
    '''
    if verbose and i%n == 0:
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

    VERBOSE = False

    # Build new collection that has fields time and tweets during that time
    print 'Binning tweets...'
    bin_tweets(coll, target, VERBOSE)

    client.close()
    return None


if __name__ == '__main__':
    main()
