from html.parser import HTMLParser
import urllib.request
import usaddress
from collections import OrderedDict
import re
import json

class HTMLTableParser(HTMLParser):
    """ This class serves as a html table parser. It is able to parse multiple
    tables which you feed in. You can access the result per .tables field.
    """

    def __init__(
            self,
            decode_html_entities=False,
            data_separator=' ',
    ):

        HTMLParser.__init__(self, convert_charrefs=decode_html_entities)

        self._data_separator = data_separator

        self._in_td = False
        self._in_th = False
        self._current_table = []
        self._current_row = []
        self._current_cell = []
        self.tables = []

    def handle_starttag(self, tag, attrs):
        """ We need to remember the opening point for the content of interest.
        The other tags (<table>, <tr>) are only handled at the closing point.
        """
        if tag == 'td':
            self._in_td = True
        if tag == 'th':
            self._in_th = True

    def handle_data(self, data):
        """ This is where we save content to a cell """
        if self._in_td or self._in_th:
            self._current_cell.append(data.strip())

    def handle_endtag(self, tag):
        """ Here we exit the tags. If the closing tag is </tr>, we know that we
        can save our currently parsed cells to the current table as a row and
        prepare for a new row. If the closing tag is </table>, we save the
        current table and prepare for a new one.
        """
        if tag == 'td':
            self._in_td = False
        elif tag == 'th':
            self._in_th = False

        if tag in ['td', 'th']:
            final_cell = self._data_separator.join(self._current_cell).strip()
            self._current_row.append(final_cell)
            self._current_cell = []
        elif tag == 'tr':
            self._current_table.append(self._current_row)
            self._current_row = []
        elif tag == 'table':
            self.tables.append(self._current_table)
            self._current_table = []


def get_table():

    web_url = 'https://dot.ca.gov/contact-us'

    # get website content
    req = urllib.request.Request(url=web_url)
    f = urllib.request.urlopen(req)
    xhtml = f.read().decode('utf-8')

    # instantiate the parser and feed it
    p = HTMLTableParser()
    p.feed(xhtml)

    office_table = p.tables[0]

    return office_table

def convert_to_json( office_table ):

    results = []

    max_size = len(office_table)

    for i in range (1,max_size):

        office_info = {}

        office_name = office_table[i][0].split("-")[0]
        office_name = office_name.rstrip(" :")
        office_info['office_name'] = office_name

        if (office_name == 'Headquarters'):
            office_link = "https://dot.ca.gov"
        else:
            office_link = "https://dot.ca.gov/caltrans-near-me/" + office_name.replace(" ","-")
        office_info['office_link'] = office_link

        address = office_table[i][1]
        address_data = usaddress.tag(address)
        address_dict = OrderedDict(address_data[0])
        office_address = address_dict['AddressNumber'] + " " + address_dict['StreetName'] + " " + address_dict['StreetNamePostType']
        if (address_dict.get('OccupancyType') != None):
            office_address += "," + address_dict['OccupancyType'] + " " + address_dict['OccupancyIdentifier']

        office_info['office_city'] = address_dict['PlaceName']
        office_info['office_state'] = address_dict['StateName']
        office_info['office_zip'] = address_dict['ZipCode']
        office_info['office_phone'] = convert_phone(office_table[i][3])
#        print(office_address,office_city, office_state, office_zip, office_phone)

        mail_address = office_table[i][2]
        m_address_data = usaddress.tag(mail_address)
        m_address_dict = OrderedDict(m_address_data[0])

        if (m_address_dict.get('USPSBoxType') != None):
            mail_address = m_address_dict['USPSBoxType'] + " " + m_address_dict['USPSBoxID']
        else:
            mail_address = m_address_dict['AddressNumber'] + " " + m_address_dict['StreetName'] + " " + m_address_dict[
                'StreetNamePostType']
            if (m_address_dict.get('OccupancyType') != None):
                mail_address += ","+ m_address_dict['OccupancyType'] + " " + m_address_dict['OccupancyIdentifier']

        office_info['mail_address'] = mail_address
        office_info['mail_city'] = m_address_dict['PlaceName']
        office_info['mail_state'] = m_address_dict['StateName']
        office_info['mail_zip'] = m_address_dict['ZipCode']
        office_info['mail_phone'] =  office_info['office_phone']

        results.append(office_info)

    return results


def convert_phone(phone_str):

    phone_numbers = ""

    for i in re.findall("[(][\d]{3}[)][ ]?[\d]{3}-[\d]{4}", phone_str):
        phone_numbers += i + ","

    phone_numbers = phone_numbers.replace("(","")
    phone_numbers = phone_numbers.replace(") ", "-")

    return phone_numbers.rstrip(",")

def write_json(json_file, office_info):

    with open(json_file, "w") as outfile:
        str_data = json.dumps(office_info,indent=2)
        outfile.write(str_data)


if __name__ == '__main__':

    result = convert_to_json(get_table())

    write_json("caltran_office_info.json", result);