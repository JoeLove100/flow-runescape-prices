import requests
from typing import List
from bs4 import BeautifulSoup


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


def _clean_name(index_name):

    index_name = index_name.replace("%27", "")  # seems to be an issue in Halloween items
    index_name = index_name.split("(")[0]

    return index_name


def get_asset_names_for_indices(indices: List[str],
                                base_url: str) -> List[str]:
    """
    get a list of distinct assets which
    appear in the selected indices
    """

    all_assets = []

    for index in indices:

        assets_in_index = _get_asset_names_for_index(index, base_url)
        all_assets.extend(assets_in_index)

    all_assets = list(set(all_assets))
    all_assets = [_clean_name(s) for s in all_assets]

    return all_assets

