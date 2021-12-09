from unittest import TestCase
from unittest.mock import Mock, patch

from updates.common.loaders import references_loader


class GetDataTest(TestCase):
    @patch("updates.common.loaders.requests.get")
    def test__result__for_single_page(self, mocked_get: Mock):
        mocked_get.side_effect = [
            Mock(
                json=Mock(return_value={"results": ["result1", "result2", "result3"]}),
                status_code=200,
            )
        ]

        results = list(references_loader("url"))

        self.assertEqual(results, ["result1", "result2", "result3"])

    @patch("updates.common.loaders.requests.get")
    def test_read_all_pages(self, mocked_get: Mock):
        """Test if read all page for paginated result"""
        mocked_get.side_effect = [
            Mock(
                json=Mock(
                    return_value={
                        "count": 5,
                        "next": "http://example.com/api/items/?limit=2&offset=2",
                        "previous": None,
                        "results": ["result1", "result2"],
                    }
                ),
                status_code=200,
            ),
            Mock(
                json=Mock(
                    return_value={
                        "count": 5,
                        "next": "http://example.com/api/items/?limit=2&offset=4",
                        "previous": "http://example.com/api/items/?limit=2",
                        "results": ["result3", "result4"],
                    }
                ),
                status_code=200,
            ),
            Mock(
                json=Mock(
                    return_value={
                        "count": 5,
                        "next": None,
                        "previous": "http://example.com/api/items/?limit=2&offset=2",
                        "results": ["result5"],
                    }
                ),
                status_code=200,
            ),
        ]

        results = list(references_loader(url="http://example.com/api/items/"))

        self.assertEqual(
            results, ["result1", "result2", "result3", "result4", "result5"]
        )
