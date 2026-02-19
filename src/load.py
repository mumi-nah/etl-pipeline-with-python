"""
Countries Data Loading Script

This script saves cleaned countries data:
- creates a connection to postgres and save the cleaned data into postgres
- optionally saves the data as a csv file

"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import logging

logging.basicConfig(filename='pipeline.log',
                    level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

load_dotenv()


def get_engine():
    """
    Create a postgres engine connection
    """

    try:
        load_dotenv()

        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        db = os.getenv('DB_NAME')

        connection_uri = f'postgresql://{user}:{password}@{host}:{port}/{db}'
        engine = create_engine(connection_uri)

        logging.info('Database engine created successfully!')
        return engine
    except Exception as e:
        logging.error(f'Failed to create engine: {e}')
        return None


def load(clean_data, engine, save_csv=False, path_to_write=None):
    """
    load clean data to postgres, and save csv version if specified

    :params clean_data: clean data variable
    :params engine: connection engine to the database
    :params save_csv (boolean):  to save csv or not
    :params path_to_write: path to write the csv to

    :return: None
    """
    try:
        if save_csv and path_to_write:
            clean_data.to_csv(path_to_write, index=False)
            logging.info(f'Data saved to csv at {path_to_write}')

        clean_data.to_sql('countries', engine, if_exists='append', index=False)
        logging.info('Data loaded into postgres succeesfully!')
    except Exception as e:
        logging.error(f'Failed to load data, {e}')


if __name__ == "__main__":
    from transform import transform

    filepath = os.getenv('RAW_DATA_PATH')
    clean_data = transform(filepath)
    path_to_write = os.getenv('PATH_TO_WRITE')
    engine = get_engine()
    if engine:
        load(
            clean_data, engine, save_csv=True,
            path_to_write=path_to_write
        )
