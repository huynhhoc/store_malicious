# database.py
import psycopg2
from psycopg2 import sql
from utils.config import DB_CONFIG

def create_tables(log = None):
    conn = None
    is_success = False
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Create URLs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS urls (
                        id SERIAL PRIMARY KEY,
                        url TEXT UNIQUE,
                        content TEXT,
                        source TEXT
                    )
                ''')
                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_urls_url ON urls (url);
                ''')

                # Create IPs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ips (
                        id SERIAL PRIMARY KEY,
                        ip TEXT UNIQUE,
                        content TEXT,
                        source TEXT
                    )
                ''')

                cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_ips_ip ON ips (ip);
                ''')
                conn.commit()
                is_success = True
    except psycopg2.Error as e:
        if log is not None:
            log.error(f"Error connecting to the database: {e}")
    finally:
        if conn is not None:
            conn.close()
        return is_success

def insert_data(items, contents, source, table, log=None):
    if not items or not contents:
        log.info("Info: The items or contents list from source {} of table {} is empty.".format(source, table))
        return
    conn = None
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                if table == 'urls':
                    query = sql.SQL(
                        "INSERT INTO urls (url, content, source) VALUES {} ON CONFLICT (url) DO UPDATE SET content = EXCLUDED.content, source = EXCLUDED.source"
                    ).format(
                        sql.SQL(', ').join(map(sql.Literal, zip(items, contents, [source] * len(items))))
                    )
                elif table == 'ips':
                    query = sql.SQL(
                        "INSERT INTO ips (ip, content, source) VALUES {} ON CONFLICT (ip) DO UPDATE SET content = EXCLUDED.content, source = EXCLUDED.source"
                    ).format(
                        sql.SQL(', ').join(map(sql.Literal, zip(items, contents, [source] * len(items))))
                    )
                cursor.execute(query)
                conn.commit()
                if log is not None:
                    log.info('Info: Table {} has been inserted/updated {} items from the source {}'.format(table, len(items), source))

    except Exception as e:
        if log is not None:
            log.error(f"Error: {e}")
    finally:
        if conn is not None:
            conn.close()

