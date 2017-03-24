# -*- coding: utf-8 -*-
# Python 2.7.3
# author: Yulin Zhu
# Date: March 2017

from bs4 import BeautifulSoup
import requests
import pandas as pd
from report import URL
import time


class StelleRequest:
    def __init__(self, URL):
        self._URL = URL

    def request_all(self):
        """
        request all latest job information and return a list consists of dictionaries.
        requests examples:
        list[200]  # all info about one offer
        list[200].find_all('div')[0].find('a')['href']  # url
        list[200].find_all('div')[0].find('a').text  # 'Stud. Hilfskraft'
        list[200].find_all('div')[0].text  # Stellebeschreibung
        list[200].find_all('div')[1].text  # Institute
        list[200].find_all('div')[2].text  # 'bewerbungsfrist'
        list[200].find('div')['class']  # class='location'

        :return: list.
        """
        soup = BeautifulSoup(requests.get(self._URL).text, "lxml")
        lists = soup.find_all('li')
        angeboten = []

        for list in lists:
            try:
                list.find('div')['class'] == 'location'
            except:
                pass
            else:
                angebot = {}
                angebot['URL'] = list.find_all('div')[0].find('a')['href']
                angebot['id'] = filter(unicode.isdigit, list.find_all('div')[0].find('a').text)
                # angebot['Name'] = list.find_all('div')[0].text
                # angebot['Anbieter'] = list.find_all('div')[1].text
                angebot['Frist'] = list.find_all('div')[2].text
                angeboten.append(angebot)

        return angeboten

    def stelle_mit_nr(self):
        Stelle_dict = dict(enumerate(self.request_all()))

        return Stelle_dict

    def fetch_all(self):
        """
        Merge details and general information together
        :return: a pandas DataFrame
        """
        Angeboten = self.request_all()
        FullDetailsOfAllAngeboten_list = []
        for i in range(1, len(Angeboten)):
            information = self.request_details(i)
            FullDetailsOfAllAngebote_dict = dict(Angeboten[i], **information)
            FullDetailsOfAllAngeboten_list.append(FullDetailsOfAllAngebote_dict)
        return pd.DataFrame(FullDetailsOfAllAngeboten_list)

    def get_single_url(self, _nr):
        url = self.stelle_mit_nr()[_nr]['URL']
        return url

    def request_details(self, _nr):
        """
        request all relervant details from stelle webpage.
        :param _id:
        :return: a dict
        """
        url = self.get_single_url(_nr)
        html_page = requests.get(url).text
        _soup = BeautifulSoup(html_page, "lxml")
        _main = _soup.find(id='main')
        # all_information = list()
        information = dict()
        try:
            information['stelle_type'] = _main.find('h1').text
            information['stelle_name'] = _main.find('h2').text
            information['Kontakter'] = _main.find_all('p')[0].text
            information['Tele'] = _main.find('dd').text
            information['Email'] = _main.find('a')['href']
            information['Anbieter'] = _main.find_all('p')[1].text
            information['Profil vom Anbieter'] = _main.find_all('p')[2].text
            information['Profil vom Bewerber'] = _main.find_all('p')[3].text
            information['Aufgaben'] = _main.find_all('p')[4].text
            information['Bewerbungsdetail'] = _main.find_all('p')[5].text
        except:
            information['stelle_type'] = _main.find('h1').text
            # information['stelle_name'] = _main.find('h2').text
            information['Kontakter'] = _main.find_all('p')[0].text
            information['Tele'] = _main.find('dd').text
            information['Email'] = _main.find('a')['href']
            information['Anbieter'] = _main.find_all('p')[1].text
            information['Profil vom Anbieter'] = _main.find_all('p')[2].text
            information['Profil vom Bewerber'] = _main.find_all('p')[3].text
            information['Aufgaben'] = _main.find_all('p')[4].text
            # information['Bewerbungsdetail'] = _main.find_all('p')[5].text
        else:
            information['stelle_type'] = _main.find('h1').text
            information['stelle_name'] = _main.find('h2').text
            information['Kontakter'] = _main.find_all('p')[0].text
            information['Tele'] = _main.find('dd').text
            information['Email'] = _main.find('a')['href']
            information['Anbieter'] = _main.find_all('p')[1].text
            information['Profil vom Anbieter'] = _main.find_all('p')[2].text
            information['Profil vom Bewerber'] = _main.find_all('p')[3].text
            information['Aufgaben'] = _main.find_all('p')[4].text
            information['Bewerbungsdetail'] = _main.find_all('p')[5].text

        # p = [i for i in _main.find_all('p')]  this doesn't work well
        # p.insert(0, None)
        # p.insert(2, _main.find('dd').text)
        # p.append(None)
        # h3 = [i for i in _main.find_all('h3')]
        # for i in range(len(p)):
        #     try:
        #         information[h3[i].text] = p[i].text
        #     except:
        #         information[h3[i].text] = p[i]
        #     else:
        #         information[h3[i].text] = p[i].text

        return information


class StelleRecorder:
    def __init__(self):
        self.id = ''
        self.url = ''
        self.name = ''
        self.Anbieter = ''
        self.frist = ''
        self.voraussetzungen = ''


if __name__ == '__main__':
    time1 = time.time()
    a = StelleRequest(URL)
    data = a.fetch_all()
    print data
    time2 = time.time()
    print "Prossecing time: {} sec.".format(time2 - time1)
