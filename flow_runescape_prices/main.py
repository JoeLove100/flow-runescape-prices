import os
import json
import logging
import pyodbc
import argparse
import pandas as pd
from datetime import datetime
from typing import Any, Dict, Tuple
from constants import Config
from asset_names_getter import get_asset_names_for_indices
from asset_data_getter import get_historic_market_data
from data_io import get_asset_data, get_index_data, upsert_asset_data, upsert_historic_data


def parse_cli_args() -> Tuple[bool, datetime]:

    parser = argparse.ArgumentParser(description="Upload Runescape asset pricing data to database")
    parser.add_argument("--refresh-assets",  dest="refresh_assets", action="store_true",
                        help="Download list of assets from the Runescape wiki")
    parser.add_argument("--start-date", help="Cutoff data of the form YYYY-MM-DD")

    args = parser.parse_args()
    refresh_assets = args.refresh_assets
    start_date = args.start_date

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start_date = datetime.now().date() + pd.offsets.MonthEnd(-1)

    return refresh_assets, start_date


def get_logger() -> logging.Logger:

    logger = logging.getLogger()
    logger.setLevel("INFO")

    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)

    return logger


def load_config() -> Dict[str, Any]:

    parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    with open(os.path.join(parent_dir, "configuration.json")) as config_json:
        main_config = json.load(config_json)

    with open(os.path.join(parent_dir, "credentials.json")) as credentials_json:
        credential = json.load(credentials_json)

    main_config.update(credential)
    return main_config


def get_cursor(config: Dict[str, Any]) -> Tuple[pyodbc.Cursor, pyodbc.Connection]:
    """
    connect to database
    """

    db_name = config[Config.DB_NAME]
    db_username = config[Config.DB_USERNAME]
    db_password = config[Config.DB_PASSWORD]

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          f'SERVER={db_name}'
                          'DATABASE=Runescape;'
                          f'UID={db_username};'
                          f'PWD={db_password}')

    cursor = conn.cursor()

    return cursor, conn


def get_data():

    logger = get_logger()
    config = load_config()
    cursor, conn = get_cursor(config)
    refresh_assets, start_date = parse_cli_args()

    logger.info("Downloading index-level data")
    selected_indices = get_index_data(cursor)
    index_data = get_historic_market_data(selected_indices, config[Config.BASE_URL_INDICES], start_date)
    logger.info("Downloaded index-level data")
    logger.info("Begin uploading historic index data to database")
    upsert_historic_data(index_data, cursor, conn, "upsert_index_historic_data.sql")
    logger.info("Historic index data uploaded to database")

    if refresh_assets:
        logger.info("Start downloading asset names for selected indices")
        assets_to_download = get_asset_names_for_indices(selected_indices, config[Config.BASE_URL_INDICES])
        logger.info("Downloaded selected asset names")
        logger.info("Begin uploading asset data to database")
        upsert_asset_data(assets_to_download, cursor, conn)
        logger.info("Asset data uploaded to database")

    all_assets = get_asset_data(cursor)
    logger.info("Get index data")
    logger.info("Downloaded index data")
    logger.info("Start downloading data for selected asset names")
    historic_data = get_historic_market_data(all_assets, config[Config.BASE_URL_ASSET], start_date)
    logger.info("Downloaded price/volume data for selected asset names")
    logger.info("Begin uploading historic asset data to database")
    upsert_historic_data(historic_data, cursor, conn, "upsert_historic_data.sql")
    logger.info("Historic asset data uploaded to database")


if __name__ == "__main__":

    get_data()
