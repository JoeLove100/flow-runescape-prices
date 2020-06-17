import os
import pyodbc
import pandas as pd


def _read_in_sql_script(script_name: str) -> str:

    current_file_path = os.path.abspath(os.path.dirname(__file__))
    query_path = os.path.join(current_file_path, "sql_scripts", script_name)

    with open(query_path) as sql_query:
        query_string = sql_query.read()

    return query_string


def upsert_index_data(index_data: pd.DataFrame,
                      db_name: str,
                      db_username: str,
                      db_password: str) -> None:
    """
    upsert the index data to the database
    """

    upsert_query = _read_in_sql_script("upsert_asset_names.sql")
    selected_values = ", ".join(str(tpl) for tpl in index_data.itertuples(index=False, name=None))
    upsert_query = upsert_query.replace("SELECTED_VALUES", selected_values)

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          f'SERVER={db_name}'
                          'DATABASE=Runescape;'
                          f'UID={db_username};'
                          f'PWD={db_password}')

    cursor = conn.cursor()
    cursor.execute(upsert_query)
    conn.commit()
