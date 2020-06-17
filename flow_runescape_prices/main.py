import json
import logging
from typing import Any, Dict

from constants import Config
from flow_runescape_prices.asset_names_getter import get_asset_names_for_indices
from flow_runescape_prices.asset_data_getter import get_all_asset_data
from flow_runescape_prices.data_upsert import upsert_index_data


def get_logger() -> logging.Logger:

    logger = logging.getLogger()
    logger.setLevel("INFO")

    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)

    return logger


def load_config() -> Dict[str, Any]:

    with open("../configuration.json") as config_json:
        main_config = json.load(config_json)

    with open("../credentials.json") as credentials_json:
        credential = json.load(credentials_json)

    main_config.update(credential)
    return main_config


def get_data():

    logger = get_logger()
    config = load_config()

    logger.info("Start downloading asset names for selected indices")
    assets_to_download = get_asset_names_for_indices(config[Config.INDICES], config[Config.BASE_URL_INDICES])
    logger.info("Downloaded selected asset names")
    logger.info("Begin uploading asset data to database")
    upsert_index_data(assets_to_download, config[Config.DB_NAME], config[Config.DB_USERNAME],
                      config[Config.DB_PASSWORD])
    logger.info("Asset data uploaded to database")


    # logger.info("Start downloading data for selected asset names")
    # all_data = get_all_asset_data(assets_to_download, config[Config.BASE_URL_ASSET])
    # logger.info("Downloaded price/volume data for selected asset names")


if __name__ == "__main__":

    get_data()


