# Scrape report info from pdf and html
A Python script that extracts information from html pages and online PDFs. Gathered information is exported in ```json``` and ```csv``` format.

## Category
Web scraping/automation/data collection.

## Purpose
A script devised to support a large migration activity of data from old Parliamentary system to new ones.

## Instructions
- Download repo
- Insert page url in ```scrape-report-info.py```
- Run ```scrape-report-info.py```

**NOTE:** a ```User-Agent``` dict needs to be added to ```make_request.py``` and ```read_pdfs.py``` request headers.

## Data collected
The following data is collected for each publication:
- Publication ID (HC number)
- Report title
- Publication date
- Report numeral (Publication ID)
- Link to PDF version of report
- Link to HTML version of report

## Dependencies
Built in Python 3.11.2 and using the following modules
- PyPDF2
- urllib
- logging
- re
- lxml
- json
- io
- sys

## Developed by
Kostas Koutoupis ([@kkoutoup](https://github.com/kkoutoup)) for the Committee Online Services (COS) team, House of Commons
