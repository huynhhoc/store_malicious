## Table of Contents

- [Description](#description)
- [DatabaseSchema](#Database Schema)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Author](#author)

# Description

The Store Malicious is a command-line application designed to efficiently process and store malicious Indicators of Compromise (IOCs) from specified data sources on the Internet into a relational database. The primary purpose is to collect and manage both IP addresses and URLs, associating them with their respective data sources.

# Database Schema

The database schema consists of two tables, urls and ips, designed to store information related to URLs and IP addresses, respectively.

* urls Table:

    id (SERIAL PRIMARY KEY): Auto-incremented unique identifier for each URL record.
    url (TEXT UNIQUE): The URL extracted from the data sources, ensuring uniqueness across records.
    content (TEXT): The content associated with the URL.
    source (TEXT): The source from which the URL was obtained.

* Indexes:

    idx_urls_url (INDEX): Index on the url column for efficient searching.

* ips Table:

    id (SERIAL PRIMARY KEY): Auto-incremented unique identifier for each IP address record.
    ip (TEXT UNIQUE): The IP address extracted from the data sources, ensuring uniqueness across records.
    content (TEXT): The content associated with the IP address.
    source (TEXT): The source from which the IP address was obtained.

* Indexes:

    idx_ips_ip (INDEX): Index on the ip column for efficient searching.

* Explanation:

    Each table has a unique identifier (id) as a primary key to ensure a unique identifier for each record.

    The url column in the urls table and the ip column in the ips table are marked as UNIQUE to enforce uniqueness across records.

    The content column stores the content associated with the URL or IP address.

    The source column indicates the source from which the URL or IP address was obtained.

    Indexes are created on the url column in the urls table and the ip column in the ips table to optimize search operations.


# Configuration

Configure your database connection and data sources in the config.py file.

## config.py

```
DB_CONFIG = {
    'dbname': 'your_database_name',
    'user': 'your_database_user',
    'password': 'your_database_password',
    'host': 'your_database_host',
    'port': 'your_database_port',
}

DATA_SOURCES = [
    'https://example.com/data_source_1',
    'https://example.com/data_source_2',
]

LOG_FILE = './logs/log.csv'

```

# Installation

To install and set up this application, follow these steps:

    Ensure you have Python 3 installed (ideally Python 3.8 or higher).

    Install required dependencies using the following command:

```
pip install -r requirements.txt

```

## Usage

``` 
python ioc_processor.py -c --save ./output_file.csv

```
