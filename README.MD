# Time-Based Blind SQLi data extractor
## Features
### Dump data
- Database name
- Table name
- Column names
- Rows / Data
### Customizable
- The default payloads have been tested on MariaDB and MySQL
- You can find more payloads [here](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)
- Add or change payloads in payloads.json
- Customizable for various use cases beyond time-based attacks
## Installation
### Clone the repo
``` bash
git clone https://github.com/aetuul/blind-dumper
cd blind-dumper
```
### Install requirements
``` bash
pip install -r requirements.txt
```
## Usage
### Find Database name
``` bash
python blind-dumper.py http://example.com/login -D
```
### Find table name
``` bash
python blind-dumper.py http://example.com/login --db <DB Name> -T
```
### Find a column name
``` bash
python blind-dumper.py http://example.com/login --db <DB Name> --table <Table Name> -C
```
### Extract data from given table and column
``` bash
python blind-dumper.py http://example.com/login --table <Table Name> --column <Column Name> -R
```