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
if __name__ == '__main__':
    unittest.main()
