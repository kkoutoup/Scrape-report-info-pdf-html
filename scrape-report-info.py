# Python modules
import re, logging, json, csv

# local modules
from make_request import make_request
from helper_functions import extract_hc_number, extract_publication_date, extract_committee_name, extract_report_numeral
from read_pdfs import get_pdf_content

def main(): 
    # logging settings
    logging.basicConfig(filename='scraping_report.log', filemode='w', format='%(levelname)s %(asctime)s\n%(message)s', datefmt='%d/%m/%Y @ %H:%M:%S', level=logging.INFO)

    def write_data_to_json_file(url):
        pdf_content = get_pdf_content(url)
        # write to file
        if pdf_content:
            try:
                with open('data.json', 'w', encoding='utf-8') as output_file:
                    json.dump(pdf_content, output_file, ensure_ascii=False, indent=4) # prevent unicode conversion so that i.e. '£' in json instead of \u00a3
            except Exception as e:
                print(f"Something went wrong when writing to file: { e }")

    # final dataset containers
    hc_numbers = []
    publication_dates = []
    committee_names = []
    report_numerals = []
    pdf_links = []
    html_links = []
    report_titles =[]

    # extract title from html page - switching to hmtl to extract report title
    def extract_report_title():
        for item in html_links:
            html_content = make_request(item, "Reading html reports")
            try:
                report_titles.append(html_content.xpath('//font[@size="+2"]//text()')[0])
            except IndexError as index_err:
                report_titles.append('Not found')
                logging.info(f"Couldn't find report title: { index_err } - check html page: { item }\n")
            except Exception as e:
                logging.info(e)

    # extract data from json file
    def extract_data_from_json_file():
        try:
            with open('data.json', 'r') as input_file:
                    data_to_json = json.loads(input_file.read())
                    for item in data_to_json:
                        # populate hc numbers
                        hc_numbers.append(extract_hc_number(item['url']))
                        # populate publication dates
                        publication_dates.append(extract_publication_date(item['content']))
                        # populate committee names
                        committee_names.append(extract_committee_name(item['content']))
                        # populate report numerals
                        report_numerals.append(extract_report_numeral(item['content']))
                        # populate pdf links
                        pdf_links.append(item['url'])
                        # build html links
                        html_links.append(re.sub(r'(i+)?.pdf', '02.htm', item['url'])) # html link can be built by modifying pdf link
        except Exception as e:
            logging.info(f"An error occured when extracting data from the following pdf: {item['url']} - {e}")
    
    #write to csv
    def write_to_csv():
        print("=> Writing to csv")
        # zip lists into single list of dicts
        combined_data = [
            { 'HC number': hc_number, 'Report title': title, 'Publication date': date, 'Committee name': name, 'Report numeral':numeral, 'PDF link': pdf_link, 'HTML link': html_link }
            for hc_number, title, date, name, numeral, pdf_link, html_link in zip(hc_numbers, report_titles, publication_dates, committee_names, report_numerals, pdf_links, html_links)
        ]
        # log combined data
        logging.info(f"{combined_data}\n")
        # write to csv
        with open('publication_data.csv', 'w', newline='') as output_file:
            fieldnames = ['HC number', 'Report title', 'Publication date', 'Committee name', 'Report numeral', 'PDF link', 'HTML link']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(combined_data)
        print("=> All done")
                    
    # run sequence
    write_data_to_json_file('https://publications.parliament.uk/pa/cm200809/cmselect/cmbis/cmbis.htm')
    extract_data_from_json_file()
    extract_report_title()
    write_to_csv()

if __name__ == "__main__":
    main()
