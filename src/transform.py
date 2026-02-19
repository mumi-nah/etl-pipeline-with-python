"""
Countries Data Transformation Script

This script transform raw extracted countries data into a clean format.
"""
# Import necessary libraries
import os
import json
import pandas as pd
from dotenv import load_dotenv
import logging

logging.basicConfig(filename='pipeline.log',
                    level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

load_dotenv()


# HELPER FUNCTION
def unnest(raw_data):
    """
    Flatten nested JSON fields, create columns for lang_count and languages

    :params raw_data: raw data
    :return: a pandas dataframe
    """
    feature_cols = []

    for data in raw_data:
        feature_cols.append([
            data.get('continents'),
            data.get('name', {}).get('official'),
            data.get('name', {}).get('common'),
            data.get('independent'),
            data.get('unMember'),
            list(data.get('languages', {}).values()),
            len(list(data.get('languages', {}))),
            data.get('idd', {}).get('root'),
            data.get('idd', {}).get('suffixes', []),
            data.get('region', ''),
            data.get('subregion'),
            data.get('area'),
            data.get('population')
        ])

    normalized_data = pd.DataFrame(
        feature_cols,
        columns=['continents', 'official_name', 'common_name', 'independent',
                 'unMember', 'languages', 'lang_count', 'root', 'suffixes',
                 'region', 'subregion', 'area', 'population']
    )
    return normalized_data


def get_cols(normalized_data):
    """
    Clean suffixes and continents columns, and create calling_code

    :param normalized_data: pandas dataframe

    :return: dataframe with clean columns and calling code column
    """
    normalized_data[['suffixes', 'continents']] = (
        normalized_data[['suffixes', 'continents']].astype(str).apply(
            lambda x: x.str.replace(r"[\[\]'\"]", "", regex=True))
    )

    normalized_data['calling_code'] = (
        normalized_data['root'] + normalized_data['suffixes']
    )
    return normalized_data


def transform(filepath):
    '''
    Run the full transformation pipeline.

    :params filepath: path to raw json file
    :return: None
    '''
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                raw_data = json.load(file)
        else:
            logging.error(f'Error: {filepath} not found')
            return None

        normalized_data = unnest(raw_data)
        normalized_data = get_cols(normalized_data)
        logging.info('Data transformed succesfully!')
        return normalized_data

    except Exception as e:
        logging.error(f'Cannot transform data: {e}')
        return None


if __name__ == "__main__":
    filepath = os.getenv('RAW_DATA_PATH')
    clean_data = transform(filepath)
