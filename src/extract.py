"""
EXTRACTING DATA FROM COUNTRIES API

This script extracts countries data from the API. It collects:
- continents
- name
- independent
- unMember
- languages
- lang_count
- root
- suffixes
- region
- subregion
- area
- population
This script outputs a raw json file with the extracted countries data.

"""

import requests
import json
import logging

logging.basicConfig(
    filename='pipeline.log',
    levelname=logging.INFO,
    format='%(levelname)s: %(message)s'
)

fieldnames = 'columns_to_be_extracted'
api_url = 'https://restcountries.com/v3.1/all?fields=fieldnames'
filepath = 'path_to_save_file'


def extract(api_url, filepath):
    '''
    Extracts data from countries api and writes to specified filepath

    :param api_url: link to the url using fields to specify fields
    :param filepath: output json file

    :return: raw json dataset from the api saved to filepath"
    '''
    try:
        response = requests.get(api_url)
        logging.info(f'request to url returned: {response.status_code}')
        response.raise_for_status()
        data = response.json()
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=2)
        logging.info(f'data successfully saved to {filepath}')
        return data

    except Exception as e:
        logging.info(f'request failed: {e}')
