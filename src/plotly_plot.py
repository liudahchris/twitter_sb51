from datetime import datetime
import plotly.plotly as py
import plotly.graph_objs as go
from plot_data import clean_df
import pandas as pd

def _make_vline(x0,c='rgb(128,128,128)',ymax=70000):
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

def make_vlines(times,colors,heights):
    vlines = [_make_vline(t,c,h) for t,c,h in zip(times,colors,heights)]
    return vlines

def _make_highlight(x,y,text,color):
    highlight = go.Scatter(
        x=[x],
        y=[y],
        mode='marker',
        text=[text],
        textposition='left',
        line=dict(color=color)
    )
    return highlight

def make_highlights(times,heights,desc,colors):
    highlights = [
        _make_highlight(t,h,text,c) for t,h,text,c in zip(times,heights,desc,colors)
    ]
    return highlights

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
    title = 'Super Bowl LI Tweet Count'
    xlabel = 'February 5th, 2017 (PST)'
    ylabel = 'Number of Tweets'


    data = []
    # Stuff for plotting
    count_data = go.Scatter(
        x=x,
        y=y,
        mode='markers+lines',
        text=labels,
        line=dict(color='rgb(82,183,75)')
    )
    data.append(count_data)

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
    data.append(halftime)

    halftime_label = go.Scatter(
        x=[datetime.strptime('2017/02/05 17:41:00',FORM)],
        y=[60000],
        text=['Lady Gaga<br>Halftime Show'],
        textposition='right',
        mode='text'
    )
    data.append(halftime_label)

    # Relevant highlight info
    red = 'rgb(209,8,8)'
    blue = 'rgb(0,10,81)'
    gray = 'rgb(128,128,128)'

    # Highlights by team colors
    colors = [gray,red,red,red,red,blue,blue,gray,blue]

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

    # Heights to put highlights
    heights = [22000,27000,38000,49000,33000,31000,44000,54000,70000]

    # Descriptions of highlights
    desc = [
        'Coin Toss / Kick Off',
        'Falcons score first touchdown<br>Falcons lead 7-0',
        'Falcons score second touchdown<br>Falcons lead 14-0',
        'Tom Brady throws an interception<br>which is returned for a touchdown\
        <br>Falcons lead 21-0',
        'Falcons score fourth touchdown<br>Falcons lead 28-3',
        'Edelman makes catch of the game',
        'Patriots score touchdown.<br>Tie game 28-28',
        'Super Bowl LI is first<br>ever to go into overtime',
        'Patriots make historic comeback<br>and become SBLI champions'
    ]

    # Make vertical lines
    vlines = make_vlines(highlight_times,colors,heights)

    highlights = make_highlights(highlight_times,heights,desc,colors)
    data += highlights

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

    fig = go.Figure(data=data,layout=layout)
    py.plot(fig,filename='sb51-twitter-analysis')
    return None

if __name__=='__main__':
    main()
