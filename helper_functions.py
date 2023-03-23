from PyPDF2 import PdfReader
import io, re, logging

# helper function - extract pdf cover text
def extract_pdf_cover_text(pdf_content):
    try:
        bytes_object = io.BytesIO(pdf_content) # turn bytes stream to file-like object
        reader = PdfReader(bytes_object)
        pdf_cover_text = reader.pages[0].extract_text().replace('\n', '-')
        return pdf_cover_text
    except Exception as e:
        logging.info(f"Something went wrong with text extraction from pdf: { e }\n")

# helper function - extract hc number from pdf link
def extract_hc_number(pdf_link):
    hc_number_regex = re.compile(r'https:\/\/publications\.parliament\.uk\/pa\/\w+\/\w+\/\w+\/\d{1,4}\/(\d{1,4})(i+)?\.pdf', re.I)
    text_match = re.match(hc_number_regex, pdf_link)
    if not text_match is None:
        if text_match.group(2) is None: # for numbers without latin numerals (i.e. 1002) second group is None
            return(text_match.group(1))
        else:
            return('-'.join(text_match.groups()).strip()) # for numbers with latin numerals (i.e. 1002-ii) both groups need to be combined
            
# helper funtion - extract publication date
def extract_publication_date(cover_text):
    publication_date_regex = re.compile(r'Published\s+on\s+(\d{1,2}\s+[JFMASOND]\w+\s+\d{1,4})', re.I)
    text_match = re.search(publication_date_regex, cover_text)
    if text_match is not None:
        return text_match.group(1)
    else:
        print("No match found for publication date")

# helper function - extract committee name
def extract_committee_name(cover_text):
    committee_name_regex = re.compile(r'0\D+House\s+of\s+Commons\s+\-([\w,\s]+)', re.I)
    text_match = re.search(committee_name_regex, cover_text)
    text_replacements = {',': '', 'and': '', '  ': ' '} # create dict with all string replacements
    if text_match is not None:
        for key,value in text_replacements.items():
            return f"{text_match.group(1).replace(key, value).rstrip()} Committee"
    else:
        print("No match found for committee name")

# helper function - extract report numeral
def extract_report_numeral(cover_text):
    report_numeral_regex = re.compile(r'\w+(st|nd|rd|th)\s+(Joint|Special)\s+Report\s+of\s+Session\D+\d{1,4}\D+\d{1,2}|\w+(st|nd|rd|th)\s+Report\s+of\D+Session\s+\d{1,4}\D+\d{1,2}', re.I)
    text_match = re.search(report_numeral_regex, cover_text)
    if text_match is not None:
        return text_match.group().replace('  -', ' ')
    else:
        print("No match found for report numeral")
