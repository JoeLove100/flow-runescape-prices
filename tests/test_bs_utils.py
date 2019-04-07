import unittest
from unittest import mock
from asset_data_getter import _get_web_page_html


class TestBSUtils(unittest.TestCase):

    class DummyResponse:

        def __init__(self, dummy_text, dummy_status_code):

            self.text = dummy_text
            self.status_code = dummy_status_code

    @mock.patch("bs_utils.requests.get")
    def test_get_web_page_html_succeeds(self, mock_get):

        # arrange

        dummy_response = TestBSUtils.DummyResponse("test text", 200)
        mock_get.return_value = dummy_response

        # act

        result = _get_web_page_html("")

        # assert

        self.assertEqual(result, "test text")

    @mock.patch("bs_utils.requests.get")
    def test_get_web_page_html_fails(self, mock_get):

        # arrange

        dummy_response = TestBSUtils.DummyResponse("test text", 400)
        mock_get.return_value = dummy_response

        # act/assert

        with self.assertRaises(ValueError):
            _get_web_page_html("")


