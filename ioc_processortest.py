import unittest
from unittest.mock import patch, Mock, MagicMock
from ioc_processor import extract_urls_ips, insert_data, create_tables

class TestIOCProcessor(unittest.TestCase):
    @patch('requests.get')
    def test_extract_urls_ips(self, mock_requests_get):
        # Mock the response from requests.get
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "http://103.29.2.134/a-r.m-5.Sakura, http://yashoda.brandwizz.in/netTimer.exe online, 123.29.2.124"
        mock_requests_get.return_value = mock_response

        # Call the function with is_content=True
        urls, ips, contents_urls, contents_ips = extract_urls_ips(mock_response, is_content=True)
        # Assert that the function returns the expected results
        self.assertEqual(urls, ["http://103.29.2.134/a-r.m-5.Sakura", "http://yashoda.brandwizz.in/netTimer.exe"])
        self.assertEqual(ips, ["123.29.2.124"])
        self.assertEqual("http://103.29.2.134/a-r.m-5.Sakura, http://yashoda.brandwizz.in/netTimer.exe online, 123.29.2.124", contents_urls[0])
        self.assertEqual("http://103.29.2.134/a-r.m-5.Sakura, http://yashoda.brandwizz.in/netTimer.exe online, 123.29.2.124", contents_urls[1])
        self.assertEqual("http://103.29.2.134/a-r.m-5.Sakura, http://yashoda.brandwizz.in/netTimer.exe online, 123.29.2.124", contents_ips[0])

    @patch('psycopg2.connect')
    def test_create_tables(self, mock_connect):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        # Mock the cursor and execute methods
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_execute = MagicMock()
        mock_cursor.execute = mock_execute
        # Call the function
        is_success = create_tables(log=None)
        self.assertEqual(is_success, True)

if __name__ == '__main__':
    unittest.main()
