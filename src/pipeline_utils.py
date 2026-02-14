import requests
import json
import pandas as pd
import os
import logging


logging.basicConfig(filename='pipeline.log',
                    level=logging.INFO,
                    format='%(levelname)s: %(message)s')


def extract(URL, savepath):
    '''
    Extracts data from countries api and writes to filepath raw_countries_data

    :param url: a string/url that calls the countries api specifying needed
    :param filepath: specified path the extracted data will be saved to
    columns using the all endpoint and fields=columns (separated by comma)
    :return: a raw dataset from the api saved to raw_countries_data"
    '''
    try:
        response = requests.get(URL)
        logging.info(f'request to url returned: {response.status_code}')
        response.raise_for_status()
        data = response.json()
        with open(savepath, 'w') as file:
            json.dump(data, file, indent=2)
        logging.info(f'data successfully saved to {savepath}')
        return data[0]

    except Exception as e:
        logging.info(f'request failed: {e}')


def transform(filepath):
    '''
    reads the extracted data and perform the following transformations:
    - create a lang_count column
    - create a column for languages separated by comma
    - extract the columns: capital, idd suffixes and continets from list
    - concatenate idd_root and idd_suffixes to form a complete dialing code
    - extract the columns that are needed

    :params raw_countries_data: the file path of the raw data
    :return: a csv file with clean and transformed data
    '''
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                raw_data = json.load(file)
        else:
            logging.info(f'error:{filepath} not found')

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
                                   'suffixes', 'region', 'subregion', 'area',
                                   'population']

        normalized_data[['suffixes', 'continents']] = normalized_data[
            ['suffixes', 'continents']].astype(str).apply(
            lambda x: x.str.replace(r"[\[\]'\"]", "", regex=True)
                )
        return normalized_data

    except Exception as e:
        logging.info(f'can not transform data{e}')


def load(clean_data):
    clean_data.to_csv(transformed_data, index=False)
    cleaan_data.to_sql = (
        name='countries_data',
        con=engine,
        if_exists='append',
        index=False
    )
