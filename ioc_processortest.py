import unittest
from unittest.mock import patch, Mock
from ioc_processor import extract_urls_ips, insert_data

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
        print ("content 0: ", contents_ips[0])
        self.assertEqual(urls, ["http://103.29.2.134/a-r.m-5.Sakura", "http://yashoda.brandwizz.in/netTimer.exe"])
        self.assertEqual(ips, ["123.29.2.124"])
        self.assertEqual("http://103.29.2.134/a-r.m-5.Sakura, http://yashoda.brandwizz.in/netTimer.exe online, 123.29.2.124", contents_urls[0])
        self.assertEqual("http://103.29.2.134/a-r.m-5.Sakura, http://yashoda.brandwizz.in/netTimer.exe online, 123.29.2.124", contents_urls[1])
        self.assertEqual("http://103.29.2.134/a-r.m-5.Sakura, http://yashoda.brandwizz.in/netTimer.exe online, 123.29.2.124", contents_ips[0])

@patch('psycopg2.connect')
@patch('psycopg2.connect.cursor')
def test_insert_data(self, mock_cursor, mock_connect):
    # Mock the database connection and cursor
    mock_conn = Mock()
    mock_cursor.return_value = mock_conn

    # Mock the execute and commit methods
    mock_execute = Mock()
    mock_conn.cursor.return_value.execute = mock_execute
    mock_conn.commit = Mock()

    # Call the function
    insert_data(["http://example.com"], ["content"], "source", "urls", log=None)

    # Assert that the SQL query is called with the correct arguments
    expected_query = "INSERT INTO urls (url, content, source) VALUES %s ON CONFLICT (url) DO UPDATE SET content = EXCLUDED.content, source = EXCLUDED.source"
    expected_values = [('http://example.com', 'content', 'source')]
    
    #mock_execute.assert_called_once_with(expected_query, expected_values)

    # Assert that commit is called
    #mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
