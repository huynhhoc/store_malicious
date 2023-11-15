import argparse
from typing import Any
import re
import logging
import sys
import csv
from typing import List, Tuple
from utils.config import LOG_FILE
#-------------------------------------------------------------------------------------------------------------------------------------------
def get_args() -> Any:
    parser = argparse.ArgumentParser()
    arg = parser.add_argument

    arg(
        "-c",
        "--content",
        default=False,
        type=bool,
        help="Set this to True if you want to save content",
        required=False,
    )
    arg(
        "-s",
        "--save",
        default= None,
        type=str,
        help="Save all contents in temp file",
        required=False,
    )

    return parser.parse_args()
def extract_ips(data) -> List[str]:
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
def extract_urls(data) -> List[str]:
    # Use regular expression to find URLs in the data
    url_pattern = re.compile(r'https?://[^\s,"]+')
    urls = url_pattern.findall(data)
    return urls

def raw_contents(items, contents) -> List[str]:
    item_line_mapping = {item: (None, None) for item in items}

    # Populate the dictionary with the line number and content for each item
    for i, line in enumerate(contents):
        for item in items:
            if item and item in line:
                item_line_mapping[item] = (i, line)

    # Create contents_items list based on the item_line_mapping using list comprehension
    contents_items = [item_line_mapping[item][1] if item_line_mapping[item][0] is not None else None for item in items]

    return contents_items

def extract_urls_ips(response, is_content)-> Tuple[List[str], List[str], List[str], List[str]]:
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

def export_to_csv(data, file_path):
    with open(file_path, 'a') as file:
        file.write(data)

def logfile():
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