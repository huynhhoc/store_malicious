# Author: Huynh Thai Hoc
import argparse
from typing import Any
import re
import logging
import sys
import os
from typing import List, Tuple
from utils.config import LOG_FILE
#-------------------------------------------------------------------------------------------------------------------------------------------
def get_args() -> Any:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser()
    arg = parser.add_argument

    arg(
        "-c",
        "--content",
        default=False,
        type=bool,
        help="Set this flag to True if you want to save content corresponding with obtained URL/IP",
        required=False,
    )
    arg(
        "-s",
        "--save",
        default= None,
        type=str,
        help="Save all contents from source into a temporary file (e.g., './logs/temps.csv')",
        required=False,
    )

    return parser.parse_args()
#-----------------------------------------------------------------------------------
def extract_ips(data) -> List[str]:
    """
    Extract IP addresses from the given data.

    Args:
        data (str): Input data.

    Returns:
        List[str]: List of extracted IP addresses.
    """
    # Remove http:// IPs
    http_pattern = re.compile(r'http://\S+')
    text = http_pattern.sub("", data)
    # Remove https:// IPs
    https_pattern = re.compile(r'https://\S+')
    text = https_pattern.sub("", text)
    # Use regular expression to find IP addresses in the data
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ips = ip_pattern.findall(text)
    return ips
#-----------------------------------------------------------------------------------
def extract_urls(data) -> List[str]:
    """
    Extract URLs from the given data.

    Args:
        data (str): Input data.

    Returns:
        List[str]: List of extracted URLs.
    """
    # Use regular expression to find URLs in the data
    url_pattern = re.compile(r'https?://[^\s,"]+')
    urls = url_pattern.findall(data)
    return urls
#-----------------------------------------------------------------------------------
def raw_contents(items, contents) -> List[str]:
    """
    Extract raw contents corresponding to the given items from the list of contents.

    Args:
        items (List[str]): List of items.
        contents (List[str]): List of contents.

    Returns:
        List[str]: List of raw contents.
    """
    item_line_mapping = {item: (None, None) for item in items}

    # Populate the dictionary with the line number and content for each item
    for i, line in enumerate(contents):
        for item in items:
            if item and item in line:
                item_line_mapping[item] = (i, line)

    # Create contents_items list based on the item_line_mapping using list comprehension
    contents_items = [item_line_mapping[item][1] if item_line_mapping[item][0] is not None else None for item in items]

    return contents_items
#-----------------------------------------------------------------------------------
def extract_urls_ips(response, is_content)-> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Extract URLs, IPs, and their corresponding contents from the response.

    Args:
        response: Response object.
        is_content (bool): Flag indicating whether to extract content.

    Returns:
        Tuple[List[str], List[str], List[str], List[str]]: URLs, IPs, contents corresponding to URLs, and contents corresponding to IPs.
    """
    try:
        data = response.text
        urls = extract_urls(data)
        ips = extract_ips(data)
        if is_content:
            contents = data.split('\n')
            contents_urls = raw_contents(urls, contents)
            contents_ips = raw_contents(ips, contents)
        else:
            contents_urls = [None] * len(urls)
            contents_ips = [None] * len(ips)
        return urls, ips, contents_urls, contents_ips
    except:
        pass
#-----------------------------------------------------------------------------------
def export_to_csv(data, file_path):
    """
    Export data to a CSV file.

    Args:
        data (str): Data to be written to the file.
        file_path (str): Path to the CSV file.
    """
    # Extract the directory path from the file_path
    directory = os.getcwd() + os.path.dirname(file_path)
    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'a') as file:
        file.write(data)
#-----------------------------------------------------------------------------------
def logfile():
    """
    Set up logging configuration and return a logger.

    Returns:
        logging.Logger: Configured logger.
    """
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s','%m-%d-%Y %H:%M:%S')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    log.addHandler(file_handler)
    log.addHandler(stdout_handler)
    return log