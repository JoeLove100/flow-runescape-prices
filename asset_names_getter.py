import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


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


def _is_asset_table_row(row):
    """
    check is a row of the assets
    table on the index page
    """

    return len(row.findAll("td", {"class": "inventory-image"})) > 0


def _extract_asset_names_from_html(parsed_html):
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


def get_asset_names_for_index(index_name):

    url = "https://runescape.wiki/w/RuneScape:Grand_Exchange_Market_Watch/" + index_name

    raw_html = _get_web_page_html(url)
    parsed_html = _get_parsed_html(raw_html)
    asset_names = _extract_asset_names_from_html(parsed_html)
    return asset_names
