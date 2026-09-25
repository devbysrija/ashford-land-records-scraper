# SearchIQS Ashford Land Records Scraper

## Overview

Python scraper for extracting Ashford, CT Land Records and exporting the data to Google Sheets.

## Features

* Land Records search
* Dynamic date range (current date − 80 days)
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

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Connect to a US VPN.
2. Open SearchIQS Ashford.
3. Search Land Records for the last 80 days.
4. Save the result pages as `page1.html` and `page2.html`.
5. Run:

```bash
python parse.py
python export.py
```

Output: `ashford_land_records.csv` and populated Google Sheet.
