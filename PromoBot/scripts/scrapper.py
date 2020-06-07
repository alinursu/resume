autor = "Ursu Alin"
import os
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

from scripts.json import JsonCommunicator

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
jsonpath = path + "bin" + slash + "json" + slash

class Scrapper:
    """
    Clasa ce defineste un obiect care este folosit pentru a prelua informatii de pe un anumit site.
    """
    def __init__(self, jsonfile, keyword, suma_maxima, cautare="normala"):
        self.jsonfile = jsonfile
        self.keyword = keyword
        self.suma_maxima = suma_maxima

        self.read_jsonfile()
        if cautare == "normala":
            if keyword == None and suma_maxima == None:
                self.link = self.jsondata["link"]
            elif suma_maxima == None and len(keyword) > 0:
                self.link = self.jsondata["link"].format(self.keyword)
            else:
                self.link = self.jsondata["link"].format(self.keyword, self.suma_maxima)
        elif cautare == "personalizata":
            if suma_maxima == None and len(keyword) > 0:
                self.link = self.jsondata["link_personalizat"].format(self.keyword)
            else:
                self.link = self.jsondata["link_personalizat"].format(self.suma_maxima, self.keyword)

    def read_jsonfile(self):
        """
        Functie ce citeste continutul unui anumit fisier .JSON selectat la definirea obiectului.
        :return:
        """
        jc = JsonCommunicator(self.jsonfile)
        self.jsondata = jc.continut_fisier()
    def get_html_code(self, link):
        """
        Functie ce preia codul HTML de la un anumit link transmis prin parametru.
        :param link:
        :return:
        """
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})
        page = urlopen(req).read()
        html = BeautifulSoup(page, "lxml")
        return html