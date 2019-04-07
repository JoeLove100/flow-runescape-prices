import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


class SeriesConstants:

    DATE = "date"
    PRICE = "price"
    VOLUME = "volume"

    ATTRIBUTE = "attribute"
    VALUE = "value"

    @classmethod
    def get_raw_columns(cls):

        raw_columns = [cls.DATE,
                       cls.PRICE,
                       cls.VOLUME]
        return raw_columns


def _get_web_page_html(page_url):
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


def _get_parsed_html(raw_html):
    """
    wrapper function for BS4 html ]
    parser
    """

    parsed_html = BeautifulSoup(raw_html, "html.parser")
    return parsed_html


def _extract_asset_chart_data(parsed_html, asset_name):
    """
    extract the asset price chart from the rune wiki
    page
    """

    charts_on_page = parsed_html.findAll("div", {"class": "GEdataprices"})
    if len(charts_on_page) == 0:
        msg = "No chart found on rune wiki page for %s" % asset_name
        raise ValueError(msg)
    elif len(charts_on_page) > 1:
        msg = "Multiple charts found on rune wiki page for %s" % asset_name
        raise ValueError(msg)
    else:
        return charts_on_page[0].get("data-data")


def _parse_timestamps_to_date(date_col):
    """
    helper method to parse the returned date column
    to actual dates
    """

    date_col = date_col.astype("int")
    date_col = date_col.apply(lambda ts: datetime.utcfromtimestamp(ts))
    date_col = date_col.dt.date
    return date_col


def _format_raw_data_as_time_series(raw_data):
    """
    reforat the raw chart data from the rune
    wiki as a pandas Series object
    """

    basic_series = pd.Series(raw_data.split("|"))
    data_series = basic_series.str.split(":", expand=True)
    data_series.columns = SeriesConstants.get_raw_columns()
    data_series[SeriesConstants.DATE] = \
        _parse_timestamps_to_date(data_series[SeriesConstants.DATE])

    return data_series


def _format_time_series(asset_time_series):
    """
    format the time series
    """

    formatted_time_series = pd.melt(asset_time_series, id_vars=SeriesConstants.DATE,
                                    var_name=SeriesConstants.ATTRIBUTE,
                                    value_name=SeriesConstants.VALUE)
    formatted_time_series.set_index([SeriesConstants.DATE, SeriesConstants.ATTRIBUTE],
                                    inplace=True)
    return formatted_time_series


def get_data_for_asset(asset_name):
    """
    download, parse and format the price and volume
    data for a given asset from the rune wiki
    """

    # download the raw data and use BS4 to get
    # the HTML in a workable format
    url = "https://runescape.fandom.com/wiki/" + asset_name
    raw_html = _get_web_page_html(url)
    parsed_html = _get_parsed_html(raw_html)

    # extract and format the price and volume data
    raw_data = _extract_asset_chart_data(parsed_html, "iron ore")
    asset_time_series = _format_raw_data_as_time_series(raw_data)
    formatted_time_series = _format_time_series(asset_time_series)

    return formatted_time_series

