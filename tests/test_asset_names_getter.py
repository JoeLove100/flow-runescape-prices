import unittest
import pandas as pd
from unittest import mock
from constants import RunescapeTimeSeries
from flow_runescape_prices.asset_names_getter import _is_asset_table_row, _clean_name, _add_display_name


class TestAssetNamesGetter(unittest.TestCase):

    def test_is_asset_table_row_false(self):
        # arrange
        mock_row = mock.MagicMock()
        mock_row.findAll = lambda x, y: []

        # act
        result = _is_asset_table_row(mock_row)

        # assert
        self.assertFalse(result)

    def test_is_asset_table_row_true(self):
        # arrange
        mock_row = mock.MagicMock()
        mock_row.findAll = lambda x, y: ["test_asset_table"]

        # act
        result = _is_asset_table_row(mock_row)

        # assert
        self.assertTrue(result)

    def test_clean_name(self):
        # arrange
        name = "test_%27asset(1)"

        # act
        result = _clean_name(name)

        # assert
        self.assertEqual("test_asset", result)

    def test_add_display_name(self):
        # arrange
        names = pd.Series(["test_asset_1", "test_asset_2"], name=RunescapeTimeSeries.PARENT_ASSET_NAME).to_frame()

        # act
        result = _add_display_name(names)

        # assert
        expected_result = pd.DataFrame({RunescapeTimeSeries.PARENT_ASSET_NAME: ["test_asset_1", "test_asset_2"],
                                        RunescapeTimeSeries.DISPLAY_NAME: ["Test Asset 1", "Test Asset 2"]})
        pd.testing.assert_frame_equal(expected_result, result)
