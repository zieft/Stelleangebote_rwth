from getdata import StelleRequest

URL = 'http://www.rwth-aachen.de/cms/root/Die-RWTH/Jobs-Ausbildung/~buym/Jobboerse/?search=&showall=1&aaaaaaaaaaaaanr=Studentische+Hilfskraft&aaaaaaaaaaaaans=&aaaaaaaaaaaaanv='


def main():
    getter = StelleRequest()
    getter.html_page()
    ListsOfAll = getter.request_all()
