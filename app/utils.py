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

def career_statistics(activities, enum='Ride'):
    output = {}
    # filter out other types of activities
    activities = activities[activities['act_type'] == enum]
    output['count'] = len(activities)
    output['distance'] = sum(activities['distance'])
    output['elevation'] = sum(activities['elevation'])
    return output
