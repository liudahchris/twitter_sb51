from datetime import datetime
from dateutil import tz
import matplotlib.pyplot as plt
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

def main():
    pass

if __name__=='__main__':
    main()
