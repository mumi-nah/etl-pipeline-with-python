"""
EXTRACTING DATA FROM COUNTRIES API

This script extracts countries data from the API. It collects:
- continents
- name
- independent
- unMember
- languages
- idd
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
    level=logging.INFO,
    format='%(asctime)s: %(levelname)s: %(message)s'
)

api_url = "https://restcountries.com/v3.1/all?fields=name,independent,\
unMember,idd,region,subregion,languages,area,population,continents"
filepath = 'data/raw_countries_data.json'


def extract(api_url, filepath):
    '''
    Extracts data from countries api and writes to specified filepath

    :param api_url: link to the url using fields to specify fields
    :param filepath: output json file

    :return: raw json dataset from the api saved to filepath"
    '''
    try:
        response = requests.get(api_url)
        logging.info(f'Request to url returned: {response.status_code}')
        response.raise_for_status()
        data = response.json()

        with open(filepath, 'w') as file:
            json.dump(data, file, indent=2)

        logging.info(f'Data successfully saved to {filepath}')
        return data

    except Exception as e:
        logging.error(f'Request failed: {e}')
        return None


if __name__ == "__main__":
    extract(api_url, filepath)
