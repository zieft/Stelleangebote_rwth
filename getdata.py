# -*- coding: utf-8 -*-
# Python 2.7.3
# author: Yulin Zhu
# Date: March 2017

from bs4 import BeautifulSoup
import requests


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
                angebot['Name'] = list.find_all('div')[0].text
                angebot['Anbieter'] = list.find_all('div')[1].text
                angebot['Frist'] = list.find_all('div')[2].text
                angeboten.append(angebot)

        return angeboten

    def stelle_mit_id(self):
        Stelle_dict = dict(enumerate(self.request_all()))

        return Stelle_dict

    def fetch_all(self):

    def fetch_record(self):
        stelle = StelleRecorder()

    def get_single_url(self, _id):
        url = self.stelle_mit_id()[_id]['URL']
        return url

    def request_details(self, _id):
        """
        request all relervant details from stelle webpage.
        :param _id:
        :return: a dict
        """
        url = 'http://www.rwth-aachen.de/cms/root/Die-RWTH/Jobs-Ausbildung/Jobboerse/~kbag/JOB-Einzelansicht/file/19519/'
        html_page = requests.get(url).text
        _soup = BeautifulSoup(html_page)
        _main = _soup.find(id='main')
        all_information = list()
        information = dict()
        information['stelle_type'] = _main.find('h1').text
        information['stelle_name'] = _main.find('h2').text
        p = [i for i in _main.find_all('p')]
        p.insert(0, None)
        p.insert(2, _main.find('dd').text)
        p.append(None)
        h3 = [i for i in _main.find_all('h3')]
        for i in range(len(p)):
            try:
                information[h3[i].text] = p[i].text
            except:
                information[h3[i].text] = p[i]
            else:
                information[h3[i].text] = p[i].text

        return information


class StelleRecorder:
    def __init__(self):
        self.id = ''
        self.url = ''
        self.name = ''
        self.Anbieter = ''
        self.frist = ''
        self.voraussetzungen = ''
