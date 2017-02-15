from collections import defaultdict
import pymongo
from clean_date import _bin_date
import numpy as np

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

def print_status(i,n=10000,verbose=True):
    '''
    Prints statement after ever n tweets are processed
    '''
    if verbose and i%n==0:
        print "{} tweets processed".format(i)
    return

def main():
    '''
    This script will take clean data and do a raw count.
    The Super Bowl started about approx. Feb 05 2017 3:30pm pst
    and ended at about Feb 05 2017 7:30pm pst.

    These translate to Feb 05 22:30:00 UTC and Feb 06 4:30:00 UTC.
    The dates should be clean (from clean_tweets.py), so comparisons
    should make sense.
    '''
    START_TIME = "2017/02/05 22:30:00"
    END_TIME = "2017/02/06 04:30:00"

    client = pymongo.MongoClient()
    db = client['clean_tweets']
    coll = db['clean_tweets']

    tweet_counts = defaultdict(int)
    VERBOSE = False

    for i,tweet in enumerate(coll.find()):
        print_status(i,verbose=VERBOSE)
        time = _bin_date(tweet['created_at'],bin_size=30)
        if time < START_TIME or time > END_TIME:
            continue
        tweet_counts[time] += 1

    client.close()

    dict_to_csv(tweet_counts,'tweet_counts.csv','time','counts')

    return None


if __name__=='__main__':
    main()
