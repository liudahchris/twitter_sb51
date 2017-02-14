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
    source_db = 'twitter_sb51'
    source_collection = 'tweets'
    target_db = 'clean_tweets'
    target_collection = 'clean_tweets'

    for tweet in client[source_db][source_collection].find():
        clean_tweet = _get_tweet_info(tweet)
        client[target_db][target_collection].insert_one(clean_tweet)

    return None

if __name__=="__main__":
    main()
