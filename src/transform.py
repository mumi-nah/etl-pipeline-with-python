"""
Countries Data Transformation Script

This script transform raw extracted countries into a clean format
by performing these steps:
"""
# Import necessary libraries
import os
import json
import pandas as pd
import logging

logging.basicCongfig(filename='pipeline.log',
                     level=logging.INFO,
                     format='%(levelname)s: %(message)s')


# HELPER FUNCTION
def unnest(raw_data):
    """
    reads the json file, and performs the following transformation:
    - Unnest the nested columns in the json file, get the other columns
    - create a lang_count colum
    - create a column for languages separated by comma
    - pass the columns to a list.
    - convert the data into a data frame,

    :params raw_data: input raw data

    :return: a pandas dataframe with columns unnested.
    """
    feature_cols = []

    for data in raw_data:
        feature_cols.append([
            data.get('continents'),
            data.get('name', {}).get('official'),
            data.get('name', {}).get('common'),
            data.get('independent'),
            data.get('unMember'),
            list(data.get('languages')),
            len(list(data.get('languages'))),
            data.get('idd', {}).get('root'),
            data.get('idd', {}).get('suffixes', []),
            data.get('region', ''),
            data.get('subregion'),
            data.get('area'),
            data.get('population')
        ])
    normalized_data = pd.DataFrame(feature_cols)
    normalized_data.columns = ['continents', 'official_name',
                               'common_name', 'independent', 'unMember',
                               'languages', 'lang_count', 'root',
                               'suffixes', 'region', 'subregion',
                               'area', 'population']
    return normalized_data


def get_cols(normalized_data):
    """
    strip special characters off suffixes and continents columns

    :param normalized_data: pandas dataframe
    :return: dataframe with clean suffixes and continents columns
    """
    normalized_data[['suffixes', 'continents']] = normalized_data[
            ['suffixes', 'continents']].astype(str).apply(
            lambda x: x.str.replace(r"[\[\]'\"]", "", regex=True)
                )

    normalized_data['calling_code'] = normalized_data['root']
    + normalized_data['suffixes']
    return normalized_data


def transform(filepath):
    '''
    confirm the data exists and run the full transformation pipeleine

    :params filepath: path to raw json file
    :return: None
    '''
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                raw_data = json.load(file)
        else:
            logging.info(f'error:{filepath} not found')
        unnest(raw_data)
        get_cols(unnest)
    except Exception as e:
        logging.info(f'can not transform data{e}')
