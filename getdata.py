# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

URL = 'http://www.rwth-aachen.de/cms/root/Die-RWTH/Jobs-Ausbildung/~buym/Jobboerse/?search=&showall=1&aaaaaaaaaaaaanr=Studentische+Hilfskraft&aaaaaaaaaaaaans=&aaaaaaaaaaaaanv='
html_page = requests.get(URL)


def make_request(html_page):
    """

    :param html_page:
    :return:
    """
    soup = BeautifulSoup(html_page.text, "lxml")
    lists = soup.find_all('li')
    angeboten = []

    for list in lists:
        try:
            if list.find('div')['class'] == 'location':
                angebot = {}
                angebot['URL'] = list.find_all('div')[0].find('a')['href']
                angebot['Stelletype'] = list.find_all('div')[0].find('a').text
                angebot['Beschreibung'] = list.find_all('div')[0].text
                angebot['Arbeitsgeber'] = list.find_all('div')[1].text
                angebot['Bewerbungsfrist'] = list.find_all('div')[2].text
        except:
            pass
        angeboten.append(angebot)

    return angeboten


    # list[200]  # 包含一条职位的所有信息
    # list[200].find_all('div')[0].find('a')['href']  # 提取职位详细网页网址
    # list[200].find_all('div')[0].find('a').text  # 提取职位种类 Studentische Hilfskraft
    # list[200].find_all('div')[0].text  # 提取职位名称
    # list[200].find_all('div')[1].text  # 提取研究所名称
    # list[200].find_all('div')[2].text  # 提取申请期限
    # list[200].find('div')['class']  # 提取class的标签location
