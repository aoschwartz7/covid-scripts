# requires pip3 install covid19dh
# package is regularly updated; update with pip3 install --upgrade covid19dh

import pandas as pd
import json
from covid19dh import covid19 #Importing the main function covid19()
from datetime import datetime

# with open("us_state_abbrev.json", "r") as read_file: # open state abbrevs for fixing df
#     state_abbrev = json.load(read_file)



def get_datahub_data():
    """ Get COVID-19 DataHub data. Make sure to update package for most recent
    results.
        Args: none yet
        Returns:
            df (DataFrame): DataFrame from DataHub search.
            src (DataFrame): DataFrame describing search sources.
    """
    df_src, src = covid19("USA", level = 2, start = datetime(2020,4,1),
                          end = "2020-05-01", verbose = False
                          )
    return df_src, src

# def clean_datahub_data(df_src:pd.DataFrame):
def clean_datahub_data(): # arg removed for testing
    """ Clean COVID-19 DataHub data.
        Args:
            df_src (DataFrame): DataHub source DataFrame.
        Returns:
            df_clean (DataFrame): Cleaned DataHub DataFrame.
    """
    df = pd.read_csv('covid_datahub.csv') # temp csv load to avoid lag with above function

    df['roi'] = df['key_alpha_2'].apply(lambda x: 'US_' + x)

    # create new DataFrame and insert choice columns with DataHub prefix (dh_)
    df_new = pd.DataFrame[columns=['ROI', 'date', 'dh_tests', 'dh_confirmed',
                                    'dh_recovered', 'dh_deaths', 'dh_hosp', 'dh_vent',
                                    'dh_icu',   ]

    # Available DataHub Fields listed below:
    #    'id', 'date', 'tests', 'confirmed', 'recovered', 'deaths',
    #    'hosp', 'vent', 'icu', 'population', 'school_closing',
    #    'workplace_closing', 'cancel_events', 'gatherings_restrictions',
    #    'transport_closing', 'stay_home_restrictions',
    #    'internal_movement_restrictions', 'international_movement_restrictions',
    #    'information_campaigns', 'testing_policy', 'contact_tracing',
    #    'stringency_index', 'iso_alpha_3', 'iso_alpha_2', 'iso_numeric',
    #    'currency', 'administrative_area_level', 'administrative_area_level_1',
    #    'administrative_area_level_2', 'administrative_area_level_3',
    #    'latitude', 'longitude', 'key', 'key_google_mobility',

    print(df.head)


# x.to_csv('covid_datahub.csv')
#
if __name__ == '__main__':
    # df = get_datahub_data()
    clean_datahub_data()
