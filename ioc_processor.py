# Author: Huynh Thai Hoc
import requests
from utils.config import DATA_SOURCES
from utils.utils import *
from Database.database import create_tables, insert_data
from utils.utils import logfile

if __name__ =='__main__':
    # Parse command-line arguments
    args = get_args()

    # Initialize logging
    log = logfile()

    # Determine whether to save content to the database
    is_save_content_to_db = args.content

    # Determine the file path for saving all contents to a temporary file
    save_all_to_temp_file = args.save

    # Create database tables
    is_success = create_tables(log)
    if not is_success:
        log.error("Cannot connect to the database or create tables has some problems. Please check the connection and database!")
        exit(1)  # Use exit code 1 for indicating a general error

    # Process each data source
    for index, source_url in enumerate(DATA_SOURCES):
        try:
            # Fetch data from the source URL
            response = requests.get(source_url)
            
            if response.status_code == 200:
                # Extract URLs, IPs, and their corresponding contents
                urls, ips, contents_urls, contents_ips = extract_urls_ips(response, is_save_content_to_db)

                # Insert data into the database
                insert_data(urls,  contents_urls, source_url, 'urls', log)
                insert_data(ips, contents_ips, source_url, 'ips', log)

                # Save information and response text to a temporary file if specified
                if save_all_to_temp_file is not None:
                    info = '{}. Found {} number of urls and {} number of ips from {}: \n'.format(index, len(urls), len(ips), source_url)
                    export_to_csv(info, save_all_to_temp_file)
                    export_to_csv(response.text, save_all_to_temp_file)
            else:
                log.warning(f"Received status code {response.status_code} while fetching data from {source_url}")
        except requests.exceptions.RequestException as e:
            log.error(f"Error during the request: {e}")

    # Script execution completed successfully
    log.info("Script execution completed successfully.")
    exit(0)  # Use exit code 0 for indicating success
