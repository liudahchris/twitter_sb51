from collections import Counter
from datetime import datetime
from dateutil import tz
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import pymongo
import seaborn as sns
import string
from unidecode import unidecode

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

def clean_tokens(tweet,stopwords,punc):
    '''
    Takes a tweet, lowers and strips punctuation, and removes stopwords and tags
    INPUT: unicode
    OUTPUT: string
    '''
    if type(tweet)==unicode:
        tweet = unidecode(tweet)
    # Lowercase, strip punctation, tokenize
    tokens = tweet.lower().translate(None,punc).split()
    # Remove stopwords and hashtags
    tokens = [token for token in tokens if token not in stopwords]
    return tokens

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

def top_n_words(docs,stopwords,punc,n=10):
    '''
    Takes a list of documents and does a word count.
    Removes stopwords and punctuation
    INPUT: List of strings, List of stings, String, int
    OUTPUT: list
    '''
    words = []
    for doc in docs:
        words += clean_tokens(doc,stopwords=stopwords,punc=punc)
    counter = Counter(words)
    n_words = [word for word,count in counter.most_common(n)]
    return n_words

def process_time(time_bin,stopwords,punc,n=10):
    '''
    '''
    tweets = time_bin['tweets']
    counts = len(tweets)
    time = convert_utc(time_bin['_id'])
    top_words = top_n_words(tweets,stopwords,punc,n)
    return (time,counts,top_words)

def main():
    '''
    '''
    STOPWORDS = [unidecode(word) for word in stopwords.words('english')]

    # Punctuation to remove
    # We'll keep '@' to look at popular users and # to look at popular tags
    PUNC = string.punctuation.translate(None,'@#')

    # Remove search words
    SEARCH_WORDS = ['#sb51','#sbli','#superbowl','super','bowl']
    STOPWORDS += SEARCH_WORDS

    # Set up mongo client
    client = pymongo.MongoClient()
    db = client['clean_tweets']
    coll = db['binned_tweets']

    PIPELINE = [{'$group':{'_id':'$time','tweets':{'$push':'$text'}}}]
    ALLOWDISKUSE = True

    FNAME = 'tweet_data.csv'
    with open(FNAME,'w') as f:
        f.write('time,count,words\n')
        for item in coll.aggregate(pipeline=PIPELINE,allowDiskUse=ALLOWDISKUSE):
            tweets = item['tweets']
            counts = len(tweets)
            time = convert_utc(item['_id'])
            top_words = top_n_words(tweets,stopwords=STOPWORDS,punc=PUNC)

    client.close()

    return None

if __name__=='__main__':
    # main()
    pass
