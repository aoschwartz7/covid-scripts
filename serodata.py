# Script for scraping and cleaning data from COVID-19 SeroHub (https://covid19serohub.nih.gov/)

from datetime import datetime
import pandas as pd
from pathlib import Path
import requests




def get_seradata(data_path: str):
    """ Gets sero data from COVID-19 SeroHub (https://covid19serohub.nih.gov/).
    Args:
        data_path(str): Full path to data directory.
    Returns:
        None
    """
    url='https://covid19serohub.nih.gov/public/COVID-19_SeroHub_DataDownload.xlsx'

    source = pd.read_excel(url)

    df = pd.DataFrame(columns=['ROI', 'Collection Period', 'Seroprevalence',
                    'Confidence Interval', 'Number of Participants (N)', 'Age',
                    'Sex', 'Race', 'Ethnicity'])


    df['ROI'] = source['Collection State'].apply(split_rois) # separate lists of states
    df['Collection Period'] = source['Collection Period'].values
    df['Seroprevalence'] = source['Seroprevalence'].values
    df['Confidence Interval'] = source['Confidence Interval'].values
    df['Number of Participants (N)'] = source['Number of Participants (N)'].values
    df['Age'] = source['Age'].values
    df['Sex'] = source['Sex'].values
    df['Race'] = source['Race'].values
    df['Ethnicity'] = source['Ethnicity'].values

    df = df.explode('ROI') # create duplicate rows for each state in list of states
    df['ROI'] = df['ROI'].apply(convert_roi) # convert ROI (eg, Alabama to US_AL)
    df.sort_values(['ROI'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(df.head)


    df.to_csv('/Users/schwartzao/Desktop/serologicalData.csv')







    # print(df.head)

    # df_sera = df_sera.explode('Collection State')
    # df_sera.to_csv('/Users/schwartzao/Desktop/test.csv')
    # alaska = df_sera[df_sera['Collection State'] == 'Alaska']
    #
    # # rslt_df = dataframe[dataframe['Percentage'] > 80]
    #
    # print(alaska['Collection State'].head(10))
    # df_sera['Collection State'] = df_sera['Collection State'].apply(convert_roi)



    # copy = df_sera['Collection State'].str.split(pat=";")

    # df_sera['Collection State'] = df_sera['Collection State'].replace(';', '-')

    # df_sera['ROI'] = df_sera['Collection State'].apply(split_rois)

    # copy = df_sera['Collection State'].apply(split_rois)


    # fix dates?
    # df_sera['Collection Period'] = df_sera['Collection Period'].apply(fix_sera_dates)
    # print(df_sera['Collection Period'].loc[0])
    # 07-01-2020/07-31-2020 = currenty format

    # split up Collection States and duplicate entries for them


def split_rois(x):
    """ Prep column for pd.explode().
    """
    try:
        if isinstance(x, str): # don't try splitting float values
            x = x.split(';')
    except:
        pass

    return x

def convert_roi(x):
    """ convert state to ROI.
    """
    try:
        if isinstance(x, str): # don't try splitting float values
            x = x.strip() # remove leading whitespace
    except:
        pass
    if x in us_state_abbrev.keys():
        x = 'US_' + us_state_abbrev[x]
    return x

# def split_rois(x):
#     """ Reformat rois under 'Collection State' into US_xx format and split cells
#     """
    # try:
    #     x = x.split(';')
    #     if len(x) > 1:
    #         for i in x:
    #             print(i)
                # if us_state_abbrev.has_key(i):
                #     print(us_state_abbrev[i])
                # i = us_state_abbrev.keys()
                # print(i)
                # if i in us_state_abbrev.keys():
                #     print(i)
                        # i = 'US_' + us_state_abbrev[i]
                        # print(i)
                # for x in i:
                #     if i in us_state_abbrev.keys():
                #         i = 'US_' + us_state_abbrev[i]
                #     print(i)


            # for k in us_state_abbrev:
            #     if
    #         # print(x)
    # except AttributeError as att_error:
    #     # print(att_error, 'Attribute error')
    #     pass












def fix_sera_dates(x):
    y = datetime.strptime(str(x), '%m-%d-%Y/%m-%d-%Y')
    return datetime.strftime(y, '%m-%d-%Y/%m-%d-%Y')

# found at https://gist.github.com/rogerallen/1583593
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}


if __name__ == '__main__':
    get_seradata('/Users/schwartzao/Desktop/workspace/covid-scripts/data')
