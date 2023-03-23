# Python modules
import re, logging

# local modules
from make_request import make_request

# collect all pdf_urls from parent page
def scrape_pdf_urls_from_page(url):
    page_content = make_request(url)
    pdf_regex = re.compile(r'(https:\/\/publications\.parliament\.uk)?/pa/[\w]{1,2}\d+\/[\w]{1,2}select/\w+\/\d+\/\d+\w?(i|ii)?\.pdf', re.I)
    all_links = page_content.xpath('//@href') # target all links on page
    pdf_links = []
    if all_links: # if all_links list not empty, only keep pdf_links
        pdf_links = [f"https://publications.parliament.uk{re.match(pdf_regex, item).group()}" for item in all_links if bool(re.match(pdf_regex, item))]
        logging.info(f"The following {len(pdf_links)} pdf links were found on the page - { url } \n\n { pdf_links }\n") # save results to file
        return pdf_links
    else:
        logging.info(f"Something went wrong with extracting pdf links on this page - { url }")