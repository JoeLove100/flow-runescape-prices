import os
import pyodbc
import functools
from typing import Dict
import pandas as pd
from constants import RunescapeTimeSeries


def _read_in_sql_script(script_name: str) -> str:
    current_file_path = os.path.abspath(os.path.dirname(__file__))
    query_path = os.path.join(current_file_path, "sql_scripts", script_name)

    with open(query_path) as sql_query:
        query_string = sql_query.read()

    return query_string


def _upsert_data(data: pd.DataFrame,
                 query_file: str,
                 cursor: pyodbc.Cursor,
                 conn: pyodbc.Connection) -> None:
    upsert_query = _read_in_sql_script(query_file)
    selected_values = ", ".join(str(tpl) for tpl in data.itertuples(index=False, name=None))
    upsert_query = upsert_query.replace("SELECTED_VALUES", selected_values)

    cursor.execute(upsert_query)
    conn.commit()


def upsert_asset_data(asset_data: pd.DataFrame,
                      cursor: pyodbc.Cursor,
                      conn: pyodbc.Connection) -> None:
    """
    need to upsert both the asset names data and
    index/asset mappings to the database
    """

    asset_names_data = asset_data[[RunescapeTimeSeries.PARENT_ASSET_NAME, RunescapeTimeSeries.DISPLAY_NAME]]
    asset_names_data.drop_duplicates(inplace=True)  # some assets appear in multiple indices
    _upsert_data(asset_names_data, "upsert_assets.sql", cursor, conn)

    asset_index_mapping = asset_data[[RunescapeTimeSeries.INDEX, RunescapeTimeSeries.PARENT_ASSET_NAME]]
    _upsert_data(asset_index_mapping, "upsert_asset_index_mapping.sql", cursor, conn)


def upsert_historic_data(historic_data: pd.DataFrame,
                         cursor: pyodbc.Cursor,
                         conn: pyodbc.Connection):
    """
    update data and upsert to ensure any revisions
    are captured
    """

    historic_data = historic_data.loc[:, [RunescapeTimeSeries.DATE, RunescapeTimeSeries.ASSET_ID,
                                          RunescapeTimeSeries.ATTRIBUTE, RunescapeTimeSeries.VALUE]]
    historic_data[RunescapeTimeSeries.DATE] = historic_data[RunescapeTimeSeries.DATE].dt.strftime("%Y-%m-%d")
    upsert_func = functools.partial(_upsert_data, query_file="upsert_historic_data.sql",
                                    cursor=cursor, conn=conn)
    historic_data.groupby([RunescapeTimeSeries.ASSET_ID]).apply(upsert_func)

    _upsert_data(historic_data, "upsert_historic_data.sql", cursor, conn)


def get_index_data(cursor: pyodbc.Cursor) -> Dict[str, int]:
    """
    get all active indices that we want to download
    assets for
    """

    index_query = _read_in_sql_script("get_indices.sql")
    cursor.execute(index_query)
    indices = cursor.fetchall()
    indices_by_id = {i[0]: i[1] for i in indices}
    return indices_by_id


def get_asset_data(cursor: pyodbc.Cursor) -> Dict[str, int]:
    """
    Read in the asset data from the SQL server
    database
    """

    asset_query = _read_in_sql_script("get_asset_data.sql")

    cursor.execute(asset_query)
    tbl_rows = cursor.fetchall()

    id_by_asset = {row[1]: row[0] for row in tbl_rows}
    return id_by_asset
