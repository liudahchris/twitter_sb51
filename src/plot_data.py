from datetime import datetime
import matplotlib.pyplot as plt
import plotly.plotly as py
import pandas as pd
import seaborn as sns

def _clean_time(time_str,form='%Y-%m-%d %H:%M:%S'):
    '''
    Takes a date/time as string and converts it to datetime
    INPUT: string
    OUTPUT: datetime obj
    '''
    # time column contains UTC component that we'll filter out
    return datetime.strptime(time_str[:-6],form)

def _clean_labels(words):
    '''
    Takes collection of words and formats them into a nice label
    INPUT: string
    OUTPUT: string
    '''
    tokens = words.split()
    n_words = len(tokens)
    text = 'Top {} Words:\n'.format(n_words)
    text += '\n'.join(words.split())
    return text


def clean_df(df):
    '''
    Takes data loaded from CSV and cleans it to be plotted
    INPUT: dataframe
    OUTPUT: dataframe
    '''
    _df = df.copy()
    _df['time'] = _df['time'].apply(_clean_time)
    _df['words'] = _df['words'].apply(_clean_labels)
    return _df

def make_plot(df,fname='../images/sb51_counts.png'):
    '''
    Saves an image of tweet counts time series to specified fname.
    '''
    # Title and label names
    TITLE = 'Super Bowl LI Tweet Counts'
    X_LABEL = 'February 5, 2017'
    Y_LABEL = 'Number of Tweets'

    # Get data
    x = df['time']
    y = df['count']

    # Start plotting
    fig = plt.figure()
    plt.plot(x,y)
    plt.title(TITLE)
    plt.xlabel(X_LABEL)
    plt.ylabel(Y_LABEL)
    plt.savefig(fname)
    return None

def plotly_plot(df):
    '''
    '''
    return None

def main():
    '''
    From process_data.py, we have written our relevant data into a csv file.
    The csv file has three columns:
        - time (in minute bins)
        - count (number of tweets per bin)
        - words (top 10 words per bin)

    First, we'll do a quick matplotlib plot and save to images directory.
    This plot will just visualize counts.

    Next, I'll work on an interactive D3 plot (using plotly). In this plot,
    you can hover over the points to also see what the most tweeted words are
    at that time.
    '''
    df = clean_df(pd.read_csv('../data/tweet_data.csv'))
    make_plot(df)
    return None

if __name__=='__main__':
    main()
