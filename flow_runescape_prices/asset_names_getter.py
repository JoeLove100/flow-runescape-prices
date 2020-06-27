import requests
import pandas as pd
from typing import List, Dict
from bs4 import BeautifulSoup
from logging import getLogger
from flow_runescape_prices.constants import RunescapeTimeSeries

logger = getLogger()


def _get_web_page_html(page_url: str) -> str:
    """
    try and request the HTML from a given
    url
    """

    response = requests.get(page_url)

    if response.status_code != 200:
        msg = "Failed to get HTML from %s" % page_url
        raise ValueError(msg)
    else:
        return response.text


def _get_parsed_html(raw_html: str) -> BeautifulSoup:
    """
    wrapper function for BS4 html ]
    parser
    """

    parsed_html = BeautifulSoup(raw_html, "html.parser")
    return parsed_html


def _is_asset_table_row(row: BeautifulSoup) -> bool:
    """
    check if the selected row is a row of the assets
    table on the index page
    """

    return len(row.findAll("td", {"class": "inventory-image"})) > 0


def _extract_asset_names_from_html(parsed_html: BeautifulSoup) -> List[str]:
    """
    extract a list of asset names contained in
    the index for
    """
    asset_names = []
    table_rows = parsed_html.findAll("tr")

    for row in table_rows:

        if _is_asset_table_row(row):
            name_cell = row.findAll("a")[1]
            asset_name = name_cell["href"].strip("/w")
            asset_names.append(asset_name)
        else:
            continue

    return asset_names


def _get_asset_names_for_index(index_name: str,
                               base_url: str) -> List[str]:

    url = base_url + index_name
    raw_html = _get_web_page_html(url)
    parsed_html = _get_parsed_html(raw_html)
    asset_names = _extract_asset_names_from_html(parsed_html)

    return asset_names


def _clean_name(index_name: str) -> str:

    index_name = index_name.replace("%27", "")  # seems to be an issue in Halloween items
    index_name = index_name.split("(")[0]

    return index_name


def _add_display_name(all_assets: pd.DataFrame) -> pd.DataFrame:

    def _to_display(name: str) -> str:
        return name.replace("_", " ").title()

    all_assets[RunescapeTimeSeries.DISPLAY_NAME] = all_assets[RunescapeTimeSeries.PARENT_ASSET_NAME].apply(_to_display)
    return all_assets


def get_asset_names_for_indices(indices: Dict[str, int],
                                base_url: str) -> pd.DataFrame:
    """
    get a list of distinct assets which
    appear in the selected indices
    """

    all_assets = []

    for index_name, index_id in indices.items():

        logger.info(f"Getting asset names for index {index_name}")
        assets_in_index = _get_asset_names_for_index(index_name, base_url)
        all_assets.extend([_clean_name(asset), index_id] for asset in assets_in_index)

    all_assets = pd.DataFrame(all_assets, columns=[RunescapeTimeSeries.PARENT_ASSET_NAME,
                                                   RunescapeTimeSeries.INDEX])
    all_assets = _add_display_name(all_assets)
    return all_assets
