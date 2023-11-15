# config.py malicious_iocs
DB_CONFIG = {
    'dbname': 'malicious_iocs',
    'user': 'postgres',
    'password': '123456',
    'host': 'localhost',
    'port': '5432',
}

DATA_SOURCES = [
    'https://urlhaus.abuse.ch/downloads/csv_recent/',
    'http://reputation.alienvault.com/reputation.data',
    'https://openphish.com/feed.txt'
]
LOG_FILE = './logs/log.csv'