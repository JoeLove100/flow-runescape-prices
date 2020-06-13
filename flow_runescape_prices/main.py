import json
import logging
from constants import Config
from flow_runescape_prices.asset_names_getter import get_asset_names_for_indices
from flow_runescape_prices.asset_data_getter import get_all_asset_data


def get_logger() -> logging.Logger:

    logger = logging.getLogger()
    logger.setLevel("INFO")

    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)

    return logger


def get_data():

    logger = get_logger()

    with open("../configuration.json") as config_json:
        config = json.load(config_json)

    logger.info("Start downloading asset names for selected indices")
    assets_to_download = get_asset_names_for_indices(config[Config.INDICES])
    logger.info("Downloaded selected asset names")

    logger.info("Start downloading data for selected asset names")
    all_data = get_all_asset_data(assets_to_download, config[Config.BASE_URL_ASSET])
    logger.info("Downloaded price/volume data for selected asset names")


if __name__ == "__main__":

    get_data()


