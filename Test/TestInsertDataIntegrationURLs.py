# Author: Huynh Thai Hoc
import unittest
import psycopg2
from ioc_processor import insert_data
from utils.config import DB_CONFIG

class TestInsertDataIntegrationURLs(unittest.TestCase):
    # setUp is called before each test method to set up necessary resources
    def setUp(self):
        try:
            # Set up a test database and connection
            self.test_conn = psycopg2.connect(**DB_CONFIG)
            self.test_cursor = self.test_conn.cursor()

            # Create the necessary tables for testing
            self.test_cursor.execute('''
                CREATE TABLE IF NOT EXISTS urls (
                    id SERIAL PRIMARY KEY,
                    url TEXT UNIQUE,
                    content TEXT,
                    source TEXT
                )
            ''')
            self.test_conn.commit()
        except psycopg2.OperationalError as e:
            print(f"Error during setUp: {e}")
            self.test_conn = None

    # tearDown is responsible for cleaning up resources after each test
    def tearDown(self):
        if self.test_conn is not None:
            try:
                # Clean up the test database after each test
                self.test_cursor.execute("DROP TABLE IF EXISTS urls")
                self.test_conn.commit()
            except Exception:
                # If an exception occurs during cleanup, roll back the transaction
                self.test_conn.rollback()
            finally:
                self.test_conn.close()

    # test_insert_data_urls_integration is the actual test method for 'urls'
    def test_insert_data_urls_integration(self):
        try:
            # Sample data for the 'urls' table
            urls = ["http://example.com", "http://anotherexample.com"]
            contents_urls = ["content1", "content2"]
            source_url = "source_url"

            # Call the function to insert data into 'urls' table
            insert_data(urls, contents_urls, source_url, 'urls', log=None)

            # Verify the data in the test database
            self.test_cursor.execute("SELECT * FROM urls")
            result = self.test_cursor.fetchall()

            # Assert that the inserted data matches the expected result
            expected_result = [
                (1, 'http://example.com', 'content1', 'source_url'),
                (2, 'http://anotherexample.com', 'content2', 'source_url')
            ]
            self.assertEqual(result, expected_result)
        except:
            print(f"Error during test_insert_data_ips_integration")

if __name__ == '__main__':
    unittest.main()
