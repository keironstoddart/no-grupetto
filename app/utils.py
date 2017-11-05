from collections import defaultdict
from sqlalchemy.inspection import inspect
import pandas as pd

def query_to_pandas(rset):
    """
    Turn a sqlalchemy query into a pandas dataframe
    Argumens:
        - rset (sqlalchemy): sqlachemy returned object
    Returns
        - result (DataFrame): dataframe representation of returned objects
    """
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    result = pd.DataFrame(result)
    return result

def second_formatter(seconds):
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%d days %d hrs %d mins %d secs' % (days, hours, minutes, seconds)
    elif hours > 0:
        return '%d hrs %d mins %d secs' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%d mins %d secs' % (minutes, seconds)
    else:
        return '%d secs' % (seconds)

def career_statistics(activities, enum='Ride'):
    output = {}
    # filter out other types of activities
    activities = activities[activities['act_type'] == enum]
    output['count'] = len(activities)
    output['distance'] = sum(activities['distance'])
    output['elevation'] = sum(activities['elevation'])
    output['speed'] = activities['speed'].mean()
    output['time'] = second_formatter(activities['time'].sum().total_seconds())
    output['avg_time'] = second_formatter(activities['time'].mean().total_seconds())
    output['max_speed'] = max(activities['max_speed'])
    earliest_ride = min(activities['date'])
    most_recent_ride = max(activities['date'])
    # average time between every 10 rides
    ride_time_range = (most_recent_ride - earliest_ride).total_seconds()/len(activities)*10
    output['ride_density'] = second_formatter(ride_time_range)
    return output
