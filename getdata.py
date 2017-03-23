# -*- coding: utf-8 -*-
# Python 2.7.3
# author: Yulin Zhu
# Date: March 2017

from bs4 import BeautifulSoup
import requests




class StelleRequest:
    def __init__(self, URL):
        self._URL = URL

    def html_page(self, URL):
        html_page = requests.get(URL)
        return html_page

    def request_all(self, html_page):
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

        :param html_page: Response from requests.get()
        :return: A list includes all te dictionaries in which contain basic information of HIWI jobs.
        """
        soup = BeautifulSoup(html_page.text, "lxml")
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
                angebot['id'] = int(filter(unicode.isdigit, list.find_all('div')[0].find('a').text))
                angebot['Name'] = list.find_all('div')[0].text
                angebot['Anbieter'] = list.find_all('div')[1].text
                angebot['Frist'] = list.find_all('div')[2].text
                angeboten.append(angebot)

        return angeboten

    def split_into_single(angeboten):

        return SingleJob
    
    def get_single_url(SingleJob):

        return url

    def request_details(URL):

        return list_of_voraussetzungen_etc

class StelleRecorder:
    def __init__(self):
        self.id = 0
        self.url = ''
        self.name = ''
        self.Anbieter = ''
        self.frist = ''
        self.voraussetzungen = ''