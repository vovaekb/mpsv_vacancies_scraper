import re
from typing import Literal

import lxml.html as html
from requests_html import HTMLSession


class VacanciesScraper:
    """Class for scraping vacancies

    ...

    Attributes
    ----------
    page : str
        a url to search for vacancies

    positions: list
        a list of resulting positions

    Methods
    -------
    search()
        Performs scraping vacancies on specified portal

    send_send_email()
        Performs sending results on specified email address
    """
    DISTRICT_CODES = {
        'Brno': '3702',
        'Praha': '3100'
    }

    def __init__(self, city: Literal['Brno', 'Praha', 'Olomouc', 'Ostrava'],
                 profession: str = 'developer'):
        # self.page = page
        self.positions = []
        self.district_code = VacanciesScraper.DISTRICT_CODES[city]
        self.profession = profession
        self.url = 'https://portal.mpsv.cz/sz/obcane/vmjedno/vmrozsir/'
        print(f'profession: {profession}')

    def search(self) -> list:
        """
        Performs actual scraping

        :return: list with resulting positions
        """

        post_data = {
            "_piref37_267288_37_267287_267287.next_page": "/vmsearch.do",
            "_piref37_267288_37_267287_267287.formtype": 3,
            "_piref37_267288_37_267287_267287.vmid": "",
            "_piref37_267288_37_267287_267287.nprokoho": "",
            "_piref37_267288_37_267287_267287.ndny": "",
            "_piref37_267288_37_267287_267287.nokres": "",
            "_piref37_267288_37_267287_267287.nsort": "",
            "_piref37_267288_37_267287_267287.ref": [],
            "_piref37_267288_37_267287_267287.kiosek": 0,
            "_piref37_267288_37_267287_267287.send": 'A',
            "_piref37_267288_37_267287_267287.ok": "Search",
            "_piref37_267288_37_267287_267287.profese": [self.profession],  # 'developer'
            "_piref37_267288_37_267287_267287.obor": "",
            "_piref37_267288_37_267287_267287.dopravaObec": "",
            "_piref37_267288_37_267287_267287.firma": "",
            "_piref37_267288_37_267287_267287.ico": "",
            "_piref37_267288_37_267287_267287.okres": self.district_code,
            "_piref37_267288_37_267287_267287.zaDny": "",
            "_piref37_267288_37_267287_267287.mzdaOd": "",
            "_piref37_267288_37_267287_267287.typMzdy": 'M',
            "_piref37_267288_37_267287_267287.sort": 2
        }

        cleanr = re.compile(r'<.*?>')

        session = HTMLSession()
        response = session.post(self.url,
                                data=post_data)
        tree = html.fromstring(response.text)
        position_elements = tree.cssselect('table.OKtbodyThDistinct tbody')
        for position_element in position_elements:
            # get details from lines using regex match
            position = {}
            occupation = position_element.cssselect('h4.vmProfese')[0].text
            position['occupation'] = occupation

            info_lines = position_element.cssselect('tr')

            for info_line in info_lines:
                if ('Company' in str(html.tostring(info_line))):
                    company_list = info_line.cssselect('b')
                    company = ''
                    if (len(company_list)):
                        company = company_list[0].text
                        position['company'] = company
                elif ('Report to' in str(html.tostring(info_line))):
                    reportto_element = info_line.cssselect('td')[2]
                    reportto_str = str(html.tostring(reportto_element,
                                                     encoding='unicode'))
                    report_to = re.sub(cleanr, '', reportto_str)
                    position['report_to'] = report_to
                elif ('Comment on vacancy:' in str(html.tostring(info_line))):
                    description_element = info_line.cssselect('td')[0]
                    description_str = str(html.tostring(description_element,
                                                        encoding='unicode'))
                    description = re.sub(cleanr, '', description_str)
                    position['description'] = description

            # print(f'company: {company}')
            # print(company.text)
            self.positions.append(position)

        # print(self.positions)
        return self.positions

    def send_email(self, email_address):
        """
        Performs sending results on specified email address
        :param email_address: email address to send results
        :return:
        """
        pass
