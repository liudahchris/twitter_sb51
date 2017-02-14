def _clean_date(date_str):
    '''
    Dates scraped from Twitter API is messy and needs to be formatted first.
    Date comes in the form:
    "Sun Feb 06 23:59:59 +0000 2017"

    clean_date takes a date in that form and returns it as a string in form:
    "2016/02/06 23:59:59"
    '''
    months = {'Jan': '01',\
              'Feb': '02',\
              'Mar': '03',\
              'Apr': '04',\
              'May': '05',\
              'Jun': '06',\
              'Jul': '07',\
              'Aug': '08',\
              'Sep': '09',\
              'Oct': '10',\
              'Nov': '11',\
              'Dec': '12'
              }
    _, month, day, time, _, year = date_str.split()
    return "{}/{}/{} {}".format(year,months[month],day,time)

def clean_dates(date_list):
    '''
    INPUT: List of dates as string, in form:
    "Sun Feb 06 23:59:59 +0000 2017"

    OUTPUT: List of dates as string, in form:
    "2016/02/06 23:59:59"
    '''
    return [_clean_date(date_str) for date_str in date_list]

def _bin_date(date_str,unit='second',bin_size=15):
    '''
    INPUT:
    date_str : date as string, in form:
    "2016/02/06 23:59:59"

    unit : {'second','minute','hour'}
    unit defines the bin-size units

    bin_size : int
    defines size of the bin

    OUTPUT: updated date str assigned to bin
    '''
    date, time = date_str.split()
    hour, minute, second = time.split(':')
    bin_ = lambda x: int(x)/bin_size * bin_size
    if unit == 'second':
        second = str(bin_(second))
    if unit == 'minute':
        minute = str(bin_(minute))
        second = '00'
    if unit == 'hour':
        hour = str(bin_(hour))
        minute = '00'
        second = '00'
    time = "{}:{}:{}".format(hour,minute,second)
    return "{} {}".format(date,time)


def bin_dates(date_list,unit='second',bin_size=15):
    '''
    INPUT:
    date_list : List of dates as string, in form:
    "2016/02/06 23:59:59"

    unit : {'second','minute','hour'}
    unit defines the bin-size units
    bin_size : int
    defines size of the bin

    OUTPUT: Updated list of dates assigned to bins
    '''
    return [_bin_date(date_str,unit,bin_size) for date_str in date_list]
