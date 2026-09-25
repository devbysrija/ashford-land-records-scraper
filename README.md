# SearchIQS Ashford Land Records Scraper

## Overview

A Python-based web scraper developed for the **Adoraxe Python Web Scraper Challenge**. The project extracts Ashford, Connecticut **Land Records** for the last **80 days** and exports the results to a CSV file and Google Sheets.

## Features

* Dynamic date range (Current Date − 80 Days)
* Land Records filtering
* Extracts:

  * Party 1
  * Party 2
  * Type
  * Book-Page
  * Date
  * Description
  * Additional Description
  * Related
* CSV export
* Google Sheets export

## Project Structure

```text
ashford-land-records-scraper/
├── scraper.py
├── parse.py
├── export.py
├── requirements.txt
├── README.md
└── ashford_land_records.csv
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Connect to a US VPN.
2. Open the SearchIQS Ashford portal.
3. Select **Land Records**.
4. Set **From Date = Today − 80 days**.
5. Set **Thru Date = Today**.
6. Save the search result pages as `page1.html` and `page2.html`.
7. Run:

```bash
python parse.py
python export.py
```

## Output

* `ashford_land_records.csv`
* Google Sheet populated through Apps Script

## Technologies

* Python 3
* Requests
* BeautifulSoup4
* Pandas
* LXML
## Google Sheet

The scraped records are exported to a public Google Sheet using `export.py`.

**Public Sheet URL:**
https://docs.google.com/spreadsheets/d/1hg-ISKA--20ao25sJhdVjyz-54YGWXwde0PRH-w4Qk8/edit?usp=sharing
