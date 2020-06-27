import requests
import pandas as pd
from logging import getLogger
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Dict, List
from constants import RunescapeTimeSeries

logger = getLogger()


def _strip_special_characters(string: str) -> str:
    """
    strip out the special characters like line
    breaks and tabs from a string
    """

    string = string.replace("\n", "")
    string = string.replace("\t", "")
    return string


def _get_web_page_html(page_url: str) -> str:
    """
    try and request the HTML from a given
    url
    """

    response = requests.get(page_url)

    if response.status_code != 200:
        msg = f"Failed to get HTML from {page_url}, returned status code {response.status_code}"
        logger.error(msg)
        raise ValueError()
    else:
        return response.text


def _get_parsed_html(raw_html: str) -> BeautifulSoup:
    """
    wrapper function for BS4 html ]
    parser
    """

    parsed_html = BeautifulSoup(raw_html, "html.parser")
    return parsed_html


def _extract_asset_chart_data(parsed_html: BeautifulSoup,
                              asset_name: str) -> str:
    """
    extract the asset price chart from the rune wiki
    page
    """

    charts_on_page = parsed_html.findAll("div", {"class": "GEdataprices"})
    if not charts_on_page:
        msg = f"No price series chart found on rune wiki page for {asset_name}"
        logger.error(msg)
        raise ValueError(msg)
    else:
        data_for_asset = charts_on_page[0].get("data-data")
        return data_for_asset


def _parse_timestamps_to_date(date_col: pd.Series) -> pd.Series:
    """
    helper method to parse the returned date column
    to actual dates
    """

    date_col = date_col.astype("int")
    date_col = date_col.apply(lambda ts: datetime.utcfromtimestamp(ts))
    date_col = date_col.dt.date
    return date_col


def _format_raw_data_as_time_series(raw_data: str) -> pd.DataFrame:
    """
    reformat the raw chart data from the rune
    wiki as a pandas Series object
    """

    basic_series = pd.Series(raw_data.split("|"))
    data_series = basic_series.str.split(":", expand=True)

    if len(data_series.columns) < 3:
        data_series[RunescapeTimeSeries.VOLUME] = None

    data_series.columns = RunescapeTimeSeries.get_raw_columns()
    data_series[RunescapeTimeSeries.DATE] = \
        _parse_timestamps_to_date(data_series[RunescapeTimeSeries.DATE])

    return data_series


def _get_time_series_by_for_asset(raw_data_for_asset: str,
                                  asset_name: str) -> pd.DataFrame:
    """
    convert the raw chart data for each sub-asset
    into a pandas DataFrame
    """

    logger.info(f"processing data for sub-asset {asset_name}")
    raw_data = raw_data_for_asset
    time_series = _format_raw_data_as_time_series(raw_data)
    return time_series


def _format_single_time_series(asset_time_series: pd.DataFrame,
                               parent_asset_name: str) -> pd.DataFrame:
    """
    format the time series
    """

    formatted_time_series = pd.melt(asset_time_series, id_vars=RunescapeTimeSeries.DATE,
                                    var_name=RunescapeTimeSeries.ATTRIBUTE,
                                    value_name=RunescapeTimeSeries.VALUE)
    formatted_time_series[RunescapeTimeSeries.PARENT_ASSET_NAME] = parent_asset_name
    formatted_time_series[RunescapeTimeSeries.DATE] = pd.to_datetime(formatted_time_series[RunescapeTimeSeries.DATE])
    formatted_time_series.dropna(subset=[RunescapeTimeSeries.VALUE], inplace=True, axis=0)
    return formatted_time_series


def _extract_sub_assets(parsed_html: BeautifulSoup,
                        asset_name: str) -> List[str]:
    """
    get the child assets for the parent asset
    if they exist, or just return the parent
    asset name if not
    """

    sub_asset_containers = parsed_html.findAll("ul", {"class": "pi-section-navigation"})

    if not sub_asset_containers:
        return [asset_name]
    else:
        container = sub_asset_containers[0]
        sub_asset_tags = container.find_all("div")
        sub_assets = [_strip_special_characters(tag.text).lower() for tag in sub_asset_tags]
        return sub_assets


def get_data_for_asset(asset_name: str,
                       base_url: str) -> pd.DataFrame:
    """
    download, parse and format the price and volume
    data for a given asset from the rune wiki
    """

    logger.info(f"getting data for parent asset {asset_name}")

    url = base_url + asset_name
    raw_html = _get_web_page_html(url)
    parsed_html = _get_parsed_html(raw_html)

    raw_data_for_asset = _extract_asset_chart_data(parsed_html, asset_name)
    asset_time_series = _get_time_series_by_for_asset(raw_data_for_asset, asset_name)
    formatted_time_series = _format_single_time_series(asset_time_series, asset_name)

    logger.info(f"downloaded data for parent asset {asset_name}")

    return formatted_time_series


def get_historic_market_data(ids_by_asset: Dict[str, int],
                             base_url: str,
                             start_date: datetime) -> pd.DataFrame:
    """
    get price and volume data for assets in the
    asset list, and return this in a pandas
    data frame
    """

    all_data = []

    for asset_name, asset_id in ids_by_asset.items():
        data_for_asset = get_data_for_asset(asset_name, base_url)
        data_for_asset[RunescapeTimeSeries.ASSET_ID] = asset_id
        data_for_asset = data_for_asset[data_for_asset[RunescapeTimeSeries.DATE] >= start_date]
        all_data.append(data_for_asset)

    data_to_return = pd.concat(all_data)
    return data_to_return
