from datetime import datetime
from dateutil import tz
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import pymongo
import seaborn as sns
import string
from unidecode import unidecode

def clean_text(tweet,stopwords,punc):
    '''
    Takes a tweet, lowers and strips punctuation, and removes stopwords and tags
    INPUT: unicode
    OUTPUT: string
    '''
    tweet = unidecode(tweet)
    # Lowercase, strip punctation, tokenize
    tokens = tweet.lower().translate(None,punc).split()
    # Remove stopwords and hashtags
    tokens = [token for token in tokens if token[0]!='#' and token not in stopwords]
    return ' '.join(tokens)

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

def main():
    '''
    '''
    client = pymongo.MongoClient()
    db = client['clean_tweets']
    coll = db['binned_tweets']

    PIPELINE = [{'$group':{'_id':'$time','tweets':{'$push':'$text'}}}]
    ALLOW_DISK_USE = True

    STOPWORDS = [unidecode(word) for word in stopwords.words('english')]
    SEARCH_WORDS = ['#sb51','#sbli','#superbowl','super','bowl']
    STOPWORDS += SEARCH_WORDS

    # Punctuation to remove
    # We'll keep @ to look at popular users and # to filter out hashtags
    PUNC = string.punctuation.translate(None,'@#')

if __name__=='__main__':
    main()
