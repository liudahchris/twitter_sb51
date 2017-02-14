from clean_date import _clean_date
import pymongo

def _get_tweet_info(tweet,attributes=['id','created_at','text']):
    '''
    Takes raw tweet data and picks out only the specified fields.
    If "created_at" in fields, function will format date into sortable
    form.

    INPUT: dictionary
    OUTPUT: dictionary with relevant and clean data
    '''
    clean_tweet = {}
    for attribute in attributes:
        clean_tweet[attribute] = tweet.get(attribute,0)

    if 'created_at' in attributes:
        clean_tweet['created_at'] = _clean_date(clean_tweet['created_at'])

    return clean_tweet


def main():
    '''
    Currently, I am only interested in looking at tweet volume over time.
    Further work may investigate sentiment analysis over time, so the parameters
    I am interested in from my tweet data are:
        - created_at
        - text
        - id (for tracking)

    To make analysis easier, I am going through the raw tweet data, cleaning it,
    and storing it in a new MongoDB and collection. The raw data will still be
    available for other analyses if desired.
    '''
    client = pymongo.MongoClient()
    src_db_name = 'twitter_sb51'
    src_coll_name = 'tweets'
    target_db_name = 'clean_tweets'
    target_coll_name = 'clean_tweets'

    src_db = client[src_db_name]
    target_db = client[target_db_name]

    for tweet in src_db[src_coll_name].find():
        clean_tweet = _get_tweet_info(tweet)
        target_db[target_coll_name].insert_one(clean_tweet)

    return None

if __name__=="__main__":
    main()
