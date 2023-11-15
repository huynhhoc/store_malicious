import unittest
import psycopg2
from ioc_processor import insert_data
from utils.config import DB_CONFIG 

class TestInsertDataIntegration(unittest.TestCase):
    def setUp(self):
        # Set up a test database and connection
        self.test_conn = psycopg2.connect(**DB_CONFIG)
        self.test_cursor = self.test_conn.cursor()

        # Create the necessary tables for testing
        self.test_cursor.execute('''
            CREATE TABLE IF NOT EXISTS ips (
                id SERIAL PRIMARY KEY,
                ip TEXT UNIQUE,
                content TEXT,
                source TEXT
            )
        ''')
        self.test_conn.commit()

    def tearDown(self):
        try:
            # Clean up the test database after each test
            self.test_cursor.execute("DROP TABLE IF EXISTS ips")
            self.test_conn.commit()
        except Exception:
            # If an exception occurs during cleanup, roll back the transaction
            self.test_conn.rollback()
        finally:
            self.test_conn.close()

    def test_insert_data_ips_integration(self):
        # Sample data for the 'ips' table
        ips = ["127.0.0.1", "192.168.1.1"]
        contents_ips = ["ip_content1", "ip_content2"]
        source_ip = "source_ip"

        # Call the function to insert data into 'ips' table
        insert_data(ips, contents_ips, source_ip, 'ips', log=None)

        # Verify the data in the test database
        self.test_cursor.execute("SELECT * FROM ips")
        result = self.test_cursor.fetchall()

        # Assert that the inserted data matches the expected result
        expected_result = [
            (1, '127.0.0.1', 'ip_content1', 'source_ip'),
            (2, '192.168.1.1', 'ip_content2', 'source_ip')
        ]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
