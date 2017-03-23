# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

URL = 'http://www.rwth-aachen.de/cms/root/Die-RWTH/Jobs-Ausbildung/~buym/Jobboerse/?search=&showall=1&aaaaaaaaaaaaanr=Studentische+Hilfskraft&aaaaaaaaaaaaans=&aaaaaaaaaaaaanv='
html_page = requests.get(URL)


def make_request(html_page):
    """
    request all latest job information and return a list consists of dictionaries.
    requests examples:
    list[200]  # 包含一条职位的所有信息
    list[200].find_all('div')[0].find('a')['href']  # url
    list[200].find_all('div')[0].find('a').text  # 'Stud. Hilfskraft'
    list[200].find_all('div')[0].text  # Stellebeschreibung
    list[200].find_all('div')[1].text  # Institute
    list[200].find_all('div')[2].text  # 'bewerbungsfrist'
    list[200].find('div')['class']  # class='location'

    :param html_page: Response from requests.get()
    :return: A list includes all the dictionaries in which contain basic information of HIWI jobs.
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
            angebot['Stelletype'] = list.find_all('div')[0].find('a').text
            angebot['Beschreibung'] = list.find_all('div')[0].text
            angebot['Arbeitsgeber'] = list.find_all('div')[1].text
            angebot['Bewerbungsfrist'] = list.find_all('div')[2].text
            angeboten.append(angebot)

    return angeboten

