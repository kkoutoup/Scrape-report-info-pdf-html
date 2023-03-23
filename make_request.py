# Python modules
import urllib.request
from urllib.error import HTTPError, URLError
from urllib.error import HTTPError, URLError
import lxml
from lxml import html
import sys

# local modules
import config

# grab content from parent page
def make_request(url, message="=> Collecting information"):
    print(message)
    my_request = urllib.request.Request(url, headers = config.user_agent) # add user agent to avoid 403 - access forbidden
    try:
        with urllib.request.urlopen(my_request) as response:
            print(f"Response status: { response.status } - { url }")
            return lxml.html.fromstring(response.read()) # turn bytes to html element
    except urllib.error.HTTPError as http_error:
        print(f"There was a problem with the request: { http_error.code } - { http_error.reason } - { http_error.headers }")
        sys.exit(1)
    except urllib.error.URLError as url_error:
        print(f"Something went wrong with the request: { url_error.reason }")
        sys.exit(1) # prevent from running rest of code in case of error
    except Exception as e:
        print(e)
        sys.exit(1)
