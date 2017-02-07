import os
import TwitterAPI
import pymongo

def make_credentials():
    '''
    Generates dictionary of Twitter access credentials stored in
    environmental variables.
    INPUT: None
    OUTPUT: dictionary
    '''
    credentials = {}
    credentials['consumer_key'] = os.environ['TWITTER_ACCESS_KEY']
    credentials['consumer_secret'] = os.environ['TWITTER_SECRET_ACCESS_KEY']
    credentials['access_token_key'] = os.environ['TWITTER_TOKEN']
    credentials['access_token_secret'] = os.environ['TWITTER_SECRET_TOKEN']
    return credentials

def main():
    # intialize mongoclient and make database and collection to store tweets
    client = pymongo.MongoClient()
    db = client.twitter_sb51
    tweets = db.tweets

    # validate api with credentials
    api = TwitterAPI.TwitterAPI(**make_credentials())

    # set query and other parameters
    QUERY = '''#sbli OR #sb51 OR #superbowl OR "super bowl"'''
    RESOURCE = 'search/tweets'
    PARAMS = {'q': QUERY,'lang':'en','count':100,'since':'2017-2-4','until':'2017-2-7'}
    r = TwitterAPI.TwitterRestPager(api,RESOURCE,PARAMS)

    # insert data into mongo
    for i,tweet in enumerate(r.get_iterator()):
        tweets.insert_one(tweet)
        if i%500==0:
            print "{} tweets stored".format(i)

    client.close()

if __name__=='__main__':
    main()
