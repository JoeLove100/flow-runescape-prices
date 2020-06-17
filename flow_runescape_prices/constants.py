class RunescapeTimeSeries:

    DATE = "date"
    PRICE = "price"
    VOLUME = "volume"

    ATTRIBUTE = "attribute"
    VALUE = "value"
    PARENT_ASSET_NAME = "parent_asset_name"
    SUB_ASSET_NAME = "sub_asset_name"
    DISPLAY_NAME = "display_name"
    INDEX = "index"

    @classmethod
    def get_raw_columns(cls):

        raw_columns = [cls.DATE,
                       cls.PRICE,
                       cls.VOLUME]
        return raw_columns


class Config:

    BASE_URL_INDICES = "base_url_indices"
    BASE_URL_ASSET = "base_url_assets"
    INDICES = "indices"
    DB_NAME = "db_name"
    DB_USERNAME = "db_username"
    DB_PASSWORD = "db_password"
