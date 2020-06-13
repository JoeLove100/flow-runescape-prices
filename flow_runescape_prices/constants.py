class RunescapeTimeSeries:

    DATE = "date"
    PRICE = "price"
    VOLUME = "volume"

    ATTRIBUTE = "attribute"
    VALUE = "value"
    PARENT_ASSET_NAME = "parent_asset_name"
    SUB_ASSET_NAME = "sub_asset_name"

    @classmethod
    def get_raw_columns(cls):

        raw_columns = [cls.DATE,
                       cls.PRICE,
                       cls.VOLUME]
        return raw_columns


class Config:

    BASE_URL_INDICES = "base_url_indices"
    BASE_URL_ASSET = "base_url_asset"
    INDICES = "indices"
