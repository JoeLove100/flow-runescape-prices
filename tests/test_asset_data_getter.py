import unittest
import pandas as pd
from unittest import mock
from datetime import date, datetime
from constants import RunescapeTimeSeries
from flow_runescape_prices.asset_data_getter import _strip_special_characters, _extract_asset_chart_data, \
    _parse_timestamps_to_date, _format_raw_data_as_time_series, _format_single_time_series, \
    _extract_sub_assets


class TestAssetDataGetter(unittest.TestCase):

    def test_strip_special_characters(self):
        # arrange
        text = "abc\tabc\n\n\tabc"

        # act
        result = _strip_special_characters(text)

        # assert
        self.assertEqual("abcabcabc", result)

    def test_extract_asset_chart_data_no_chart(self):
        # arrange
        mock_parsed_html = mock.MagicMock()
        mock_parsed_html.findAll = lambda x, y: None

        with self.assertRaises(ValueError):
            _extract_asset_chart_data(mock_parsed_html, "test_asset")

    def test_extract_asset_chart_data_chart_exists(self):
        # arrange
        mock_parsed_html = mock.MagicMock()
        mock_parsed_html.findAll = lambda x, y: [{"data-data": "test_data"}]

        # act
        result = _extract_asset_chart_data(mock_parsed_html, "test_asset")

        # assert
        self.assertEqual("test_data", result)

    def test_parse_timestamp_to_date(self):
        # arrange
        timestamps = pd.Series([1593247370, 1263513600])

        # act
        result = _parse_timestamps_to_date(timestamps)

        # assert
        expected_result = pd.Series([date(2020, 6, 27), date(2010, 1, 15)])
        pd.testing.assert_series_equal(expected_result, result, check_dtype=False)

    def test_format_raw_data_as_time_series(self):
        # arrange
        raw_data = "1593129600:135:1000|1593247370:140:1000"

        # act
        result = _format_raw_data_as_time_series(raw_data)

        # assert
        expected_series = pd.DataFrame({RunescapeTimeSeries.DATE: [date(2020, 6, 26), date(2020, 6, 27)],
                                        RunescapeTimeSeries.PRICE: ["135", "140"],
                                        RunescapeTimeSeries.VOLUME: ["1000", "1000"]})
        pd.testing.assert_frame_equal(expected_series, result)

    def test_format_single_time_series(self):
        # arrange
        all_dates = [date(2020, 1, 31), date(2020, 2, 1), date(2020, 2, 2)]
        test_time_series = pd.DataFrame({RunescapeTimeSeries.DATE: all_dates,
                                         RunescapeTimeSeries.PRICE: [120, 122, 118],
                                         RunescapeTimeSeries.VOLUME: [1000, None, None]})

        # act
        result = _format_single_time_series(test_time_series, "test_asset")

        # assert
        expected_dates = [datetime(2020, 1, 31), datetime(2020, 2, 1), datetime(2020, 2, 2), datetime(2020, 1, 31)]
        expected_result = pd.DataFrame({RunescapeTimeSeries.DATE: expected_dates,
                                        RunescapeTimeSeries.ATTRIBUTE: [RunescapeTimeSeries.PRICE] * 3 +
                                        [RunescapeTimeSeries.VOLUME],
                                       RunescapeTimeSeries.VALUE: [120, 122, 118, 1000],
                                       RunescapeTimeSeries.PARENT_ASSET_NAME: ["test_asset"] * 4})
        pd.testing.assert_frame_equal(expected_result, result, check_dtype=False)

    def test_extract_sub_assets_no_sub_assets(self):
        # arrange
        mock_parsed_html = mock.MagicMock()
        mock_parsed_html.findAll = lambda x, y: None

        # act
        result = _extract_sub_assets(mock_parsed_html, "test_asset")

        # assert
        self.assertSequenceEqual(["test_asset"], result)

