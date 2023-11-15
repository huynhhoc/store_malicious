# main.py
import requests
from utils.config import DATA_SOURCES
from utils.utils import *
from Database.database import create_tables, insert_data
from utils.utils import logfile


if __name__ =='__main__':
    args = get_args()
    log = logfile()
    is_save_content_to_db = args.content
    save_all_to_temp_file = args.save
    is_success = create_tables(log)
    if not is_success:
        log.info("Cannot connect to the database or create tables has some problems. Please check the connection and database!")
        exit()
    for index, source_url in enumerate(DATA_SOURCES):
        try: 
            response = requests.get(source_url)
            if response.status_code == 200:
                urls, ips, contents_urls, contents_ips = extract_urls_ips(response, is_save_content_to_db)
                insert_data(urls,  contents_urls, source_url,'urls', log)
                insert_data(ips, contents_ips, source_url, 'ips', log)
                if save_all_to_temp_file is not None:
                    info = '{}. Found {} number of urls and {} number of ips from {}: \n'.format(index, len(urls), len(ips), source_url)
                    export_to_csv(info, save_all_to_temp_file)
                    export_to_csv(response.text, save_all_to_temp_file)
        except requests.exceptions.RequestException as e:
            log.error(f"Error during the request: {e}")