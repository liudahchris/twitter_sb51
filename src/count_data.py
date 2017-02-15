from collections import defaultdict
import pymongo
from clean_date import _bin_date
from datetime import datetime
from dateutil import tz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_time_counts(count_dict,outname='../images/time_counts.png'):
    '''
    INPUT: dictionary where keys are datetimes and values are counts
    OUTPUT: none
    '''
    X,y = [],[]
    for key in sorted(count_dict):
        X.append(key)
        y.append(count_dict[key])

    plt.plot(X,y)
    plt.savefig(outname)

    return None


def convert_utc(time_str,time_format="%Y/%m/%d %H:%M:%S",zone='America/Los_Angeles'):
    '''
    INPUT: date string in form "%Y/%m/%d %H:%M:%S" in UTC
    OUTPUT: datetime object in PST
    '''
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(zone)

    utc_time = datetime.strptime(time_str,time_format)
    utc_time = utc_time.replace(tzinfo=from_zone)

    return utc_time.astimezone(to_zone)


def dict_to_csv(d,outname,key_names='col1',val_names='col2'):
    with open(outname,'w') as f:
        f.write('{}, {}\n'.format(key_names,val_names))
        for key in sorted(d):
            f.write('{}, {}\n'.format(key,d[key]))

    return None

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

    for i,tweet in enumerate(coll.find()):
        # if i%10000==0:
        #     print "{} tweets loaded".format(i)
        time = _bin_date(tweet['created_at'],bin_size=30)
        if time < START_TIME or time > END_TIME:
            continue
        # time = convert_utc(time)
        tweet_counts[time] += 1

    client.close()

    dict_to_csv(tweet_counts,'tweet_counts.csv','time','counts')

    return None


if __name__=='__main__':
    main()
