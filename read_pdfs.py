# Python modules
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.error import HTTPError, URLError
import logging, sys

# local modules
from helper_functions import extract_pdf_cover_text
from scrape_pdf_links import scrape_pdf_urls_from_page

# read pdfs and store data
def get_pdf_content(url):
    pdf_links = scrape_pdf_urls_from_page(url) # collect all pdf links
    print("=> Reading pdfs")
    # data container
    pdf_content = []
    # loop through links, extract text from first page and store in list
    for item in pdf_links:
        my_request = urllib.request.Request(item, headers = {  }) # add user agent to avoid 403 - access forbidden  
        try:
            with urllib.request.urlopen(my_request) as response: 
                print(f"Response status: { response.status } - { item }")
                if response.status == 200:
                    pdf_content.append(
                        {
                            "url": item,
                            "content": extract_pdf_cover_text(response.read())
                        }
                    )
                else:
                    logging.info(f"No content extracted for pdf link - { item }\n")
        except urllib.error.HTTPError as http_error:
            print(f"There was a problem with the request: { http_error.code } - { http_error.reason } - { http_error.headers }")
            sys.exit(1)     
        except urllib.error.URLError as url_error:
            print(f"Something went wrong with the request: { url_error.reason }")
            sys.exit(1) # prevent from running rest of code in case of error
        except Exception as e:
            print(e)
            sys.exit(1)
    logging.info(f"PDF content: \n {pdf_content}\n")
    return pdf_content