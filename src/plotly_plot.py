from datetime import datetime
import plotly.plotly as py
import plotly.graph_objs as go
from plot_data import clean_df
import pandas as pd

def make_vline(x0,c='rgb(128,128,128)',ymax=70000):
    d = {
        'type': 'line',
        'x0': x0,
        'x1': x0,
        'y0': 0,
        'y1': ymax,
        'line': {
            'color': c,
            'width': 2,
            'dash': 'dashdot',
        }
    }
    return d

def make_highlight(x,y,text,color):
    highlight = go.Scatter(
        
    )

def main():
    '''
    A script for generating a more interesting plotly plot
    '''
    # Load data
    FNAME = '../data/tweet_data_2.csv'
    df = clean_df(pd.read_csv(FNAME))
    x = df['time']
    y = df['count']
    labels = df['words']

    # Form for datetime conversion
    FORM = '%Y/%m/%d %H:%M:%S'

    # Titles and labels
    title = 'Super Bowl LI Tweet Count test 2'
    xlabel = 'February 5th, 2017 (PST)'
    ylabel = 'Number of Tweets'

    # Stuff for plotting
    count_data = go.Scatter(
        x=x,
        y=y,
        mode='markers+lines',
        text=labels
    )

    # Highlight Locations
    highlight_times = [
        datetime.strptime('2017/02/05 15:37:00',FORM),\
        datetime.strptime('2017/02/05 16:17:00',FORM),\
        datetime.strptime('2017/02/05 16:30:00',FORM),\
        datetime.strptime('2017/02/05 16:47:00',FORM),\
        datetime.strptime('2017/02/05 17:54:00',FORM),\
        datetime.strptime('2017/02/05 19:00:00',FORM),\
        datetime.strptime('2017/02/05 19:07:00',FORM),\
        datetime.strptime('2017/02/05 19:16:00',FORM),\
        datetime.strptime('2017/02/05 19:27:00',FORM)
    ]

    heights = [22000,27000,38000,49000,33000,31000,44000,54000,70000]

    highlights = go.Scatter(
        x=highlight_times,
        y=heights,
        mode='marker',
        text=['text']*9,
        textposition='left'
    )

    # Halftime Show
    halftime = go.Scatter(
        x=[
            datetime.strptime('2017/02/05 17:20:00',FORM),\
            datetime.strptime('2017/02/05 17:41:00',FORM)
           ],
        y=[70000,70000],
        fill='tozeroy',
        mode='none'
    )

    halftime_label = go.Scatter(
        x=[datetime.strptime('2017/02/05 17:41:00',FORM)],
        y=[60000],
        text=['Lady Gaga<br>Halftime Show'],
        textposition='right',
        mode='text'
    )

    # Make vertical lines
    red = 'rgb(209,8,8)'
    blue = 'rgb(0,10,81)'
    gray = 'rgb(128,128,128)'
    colors = [gray,red,red,red,red,blue,blue,gray,blue]
    vlines = [make_vline(t,c,h) for t,c,h in zip(highlight_times,colors,heights)]

    # Layouts and vertical lines
    layout = go.Layout(
        title=title,
        xaxis=dict(title=xlabel),
        yaxis=dict(title=ylabel),
        hovermode='closest',
        showlegend=False,
        # Vertical lines
        shapes=vlines
    )


    # Collect all data
    data = [count_data,highlights,halftime,halftime_label]

    fig = go.Figure(data=data,layout=layout)
    py.plot(fig,filename='sb-test')
    return None


    return None

if __name__=='__main__':
    main()
