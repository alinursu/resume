autor = "Ursu Alin"
import os
import sys

from scripts import db
from scripts import utils
from scripts.SPORTVISION import sportivision_string
from scripts.debug import Debug, Verificare_Debug, Logger
from scripts.htmlcreator import creatorHTML_sportvision, HTML_adaugare_regasire
from scripts.scrapper import Scrapper

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
jsonfn = "sportvision.json"

html_part_link = {"Incaltaminte Sport Barbati":"pantofi-sport/barbati",
                  "Incaltaminte Sport Femei":"incaltaminte/femei+unisex/promotii",
                  "Incaltaminte Sport Copii":"incaltaminte/baieti+fete/promotii",
                  "Produse Adidas":"produse/adidas/promotii",
                  "Produse Champion":"produse/champion/promotii",
                  "Produse Converse":"produse/converse/promotii",
                  "Produse Lonsdale":"produse/lonsdale/promotii",
                  "Produse New Balance":"produse/new-balance/promotii",
                  "Produse Nike":"produse/nike/promotii",
                  "Produse Puma":"produse/puma/promotii",
                  "Produse Reebok":"produse/reebok/promotii",
                  "Produse Under Armour":"produse/under-armour/promotii",
                  "Produse Timberland": "produse/timberland/promotii"}

def Sportvision(categorie, pagini, cautare="normala"):
    """
    Functie ce preia informatii despre produsele aflate la reducere dintr-o anumita categorie, de pe un anumit numar de
    pagini, de pe site-ul Sportvision.
    :param categorie:
    :return:
    """
    log = Logger()
    debug = Verificare_Debug()
    if cautare == "normala":
        keyword = html_part_link[categorie]
        s = Scrapper(jsonfn, keyword, None)
    elif cautare == "personalizata":
        s = Scrapper(jsonfn, categorie, None, cautare="personalizata")
    html = s.get_html_code(s.link)
    log.scriere("Preiau date de pe {}.".format(s.link))

    # Preiau numarul maxim de pagini
    pagini_max = 0
    for el in html.select(s.jsondata["pagini"]["tag"]):
        try:
            if el[s.jsondata["pagini"]["tip"]] == s.jsondata["pagini"]["termen"]:
                for e in el.select(s.jsondata["pagini"]["tag2"]):
                    try:
                        if pagini_max < int(e.text):
                            pagini_max = int(e.text)
                    except:
                        pass
                break
        except:
            pass
    #  Setez numarul de pagini de pe care se vor prelua produse, comparand datele introduse de utilizator cu numarul
    # maxim de pagini admis de cautare
    if pagini == None:
        pagini = 10
    if pagini > pagini_max:
        pagini = pagini_max

    # Preiau produsele de pe fiecare pagina
    hrefs = []
    for i in range(0, pagini):
        if cautare == "normala":
            html = s.get_html_code(s.jsondata["link_pagina"].format(keyword,i))
        elif cautare == "personalizata":
            html = s.get_html_code(s.jsondata["link_personalizat_pagina"].format(i, categorie))
        # Preiau lista de produse
        container = ""
        for el in html.select(s.jsondata["container"]["tag"]):
            try:
                if el[s.jsondata["container"]["tip"]] == s.jsondata["container"]["termen"]:
                    container = el
                    break
            except:
                pass

        # Preiua link-urile spre produse
        for el in container.select(s.jsondata["produs"]["tag"]):
            try:
                if el[s.jsondata["produs"]["tip"]] == s.jsondata["produs"]["termen"]:
                    _ = []
                    # Nu mai verific daca produsele se afla la reducere pentru ca au fost aplicate deja filtre
                    for e in el.select(s.jsondata["produs"]["link"]["tag"]):
                        try:
                            _.append(e[s.jsondata["produs"]["link"]["arg"]])
                        except:
                            pass
                    hrefs.append(_[-1])
            except:
                pass

    # Pentru fiecare produs, preiau informatiile necesare
    for href in hrefs:
        log.scriere("Preiau informatiile de pe {}.".format(href))
        if debug == True:
            Debug(href, 0)
        info = {}
        html = s.get_html_code(href)

        # Preiau titlul produsului
        for el in html.select(s.jsondata["data"]["titlu"]["tag"]):
            try:
                if el[s.jsondata["data"]["titlu"]["tip"]] == s.jsondata["data"]["titlu"]["termen"]:
                    info["titlu"] = el.text
                    break
            except:
                pass

        # Preiau pretul nou, pretul vechi si discount-ul produsului
        _ = {}
        for el in html.select(s.jsondata["data"]["pret"]["nou"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["nou"]["tip"]] == s.jsondata["data"]["pret"]["nou"]["termen"]:
                    _["nou"] = sportivision_string.formare_pret(el.text)
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["pret"]["vechi"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["vechi"]["tip"]] == s.jsondata["data"]["pret"]["vechi"]["termen"]:
                    _["vechi"] = sportivision_string.formare_pret(el.text)
                    break
                elif el[s.jsondata["data"]["pret"]["vechi2"]["tip"]] == s.jsondata["data"]["pret"]["vechi2"]["termen"]:
                    _["vechi"] = sportivision_string.formare_pret(el.text)
                    break
            except:
                pass
        __ = []
        for el in html.select(s.jsondata["data"]["pret"]["discount"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["discount"]["tip"]] == s.jsondata["data"]["pret"]["discount"]["termen"]:
                    __.append(el.text)
            except:
                pass
        _["discount"] = __[-1]
        info["pret"] = _

        # Preiau descrierea produsului
        desc = None
        for el in html.select(s.jsondata["data"]["descriere"]["tag"]):
            try:
                if el[s.jsondata["data"]["descriere"]["tip"]] == s.jsondata["data"]["descriere"]["termen"]:
                    desc = el.text
                    break
            except:
                pass
        if desc != None:
            info["descriere"] = sportivision_string.formare_descriere(desc)
        else:
            for el in html.select(s.jsondata["data"]["structura"]["tag"]):
                try:
                    if el[s.jsondata["data"]["structura"]["tip"]] == s.jsondata["data"]["structura"]["termen"]:
                        info["descriere"] = sportivision_string.formare_descriere(el.text)
                        break
                except:
                    pass

        # Preiau specificatiile produsului
        __ = {}
        for el in html.select(s.jsondata["data"]["specs"]["tag"]):
            try:
                if el[s.jsondata["data"]["specs"]["tip"]] == s.jsondata["data"]["specs"]["termen"]:
                    _ = el.select(s.jsondata["data"]["specs"]["tag2"])

                    ___ = None
                    for e in _[0].select(s.jsondata["data"]["specs"]["tag3"]):
                        if ___ == None:
                            ___ = e.text
                        else:
                            __[___] = e.text
                            ___ = None
                    break
            except:
                pass
        info["specs"] = __

        # Salvez link-ul catre produs
        info["link"] = href

        # Preiau imaginile produsului
        imgs = []
        for el in html.select(s.jsondata["data"]["imagini"]["tag"]):
            try:
                if el[s.jsondata["data"]["imagini"]["tip"]] == s.jsondata["data"]["imagini"]["termen"]:
                    for e in el.select(s.jsondata["data"]["imagini"]["imagine"]["tag"]):
                        imgs.append(e[s.jsondata["data"]["imagini"]["imagine"]["arg"]])
                    break
            except:
                pass
        # Descarc imaginile
        try:
            _ = info["titlu"].split(" ")
        except:
            _ = ""
        imgname = ""
        try:
            for i in range(0, 10):
                imgname = imgname + _[i] + " "
        except:
            pass
        imgname = imgname + "- "
        IMGS = []
        log.scriere("Descarc {} imagini.".format(len(imgs)))
        for i in range(0, len(imgs)):
            try:
                utils.download_imagine(imgs[i], imgname + str(i))
                IMGS.append(imgname + str(i) + ".{}".format(imgs[i].split("/")[-1].split(".")[-1]))
            except:
                if debug == True:
                    Debug("Eroare download {}".format(str(imgs[i])), 2)
        if len(IMGS) > 0:
            info["imagini"] = IMGS

        # Verific daca exista toate datele si, daca da, creez fisierul HTML
        if debug == True:
            Debug(str(info.keys()), 0)
            Debug(str(info["pret"].keys()), 0)
        kw = {"titlu":None, "pret":["vechi", "nou", "discount"], "descriere":None, "specs": None, "imagini":None, "link":None}
        if utils.verificare_date(info, kw) == False:
            # Daca nu sunt toate datele necesare, sterg imaginile produsului
            if debug == True:
                Debug("Date insuficiente", 2)
            utils.stergere_set_imagini(imgname)
        else:
            log.scriere("Salvez fisierul HTML.")
            creatorHTML_sportvision(info)
            d = db.Database("sportvision")
            d.initializare_conexiune()
            x = d.cautare_date_link(info["link"])
            if len(x) == 0:
                _ = d.cautare_ultima_data(info["link"])
                if _ == 0:
                    d.adaugare_date({"link": info["link"], "pret": info["pret"]["nou"]})
                else:
                    if db.comparare_data_actuala_cu_ultima(_) == 1:
                        d.adaugare_date({"link": info["link"], "pret": info["pret"]["nou"]})
                d.inchidere_conexiune()
            else:
                regasit = db.alegere_pretul_minim(x)
                if regasit["pret"] < db.formare_int_pret(info["pret"]["nou"]):
                    if debug == True:
                        Debug("Produsul a fost regasit!", 0)
                    HTML_adaugare_regasire(info["titlu"], regasit["data"], regasit["pret"])
                _ = d.cautare_ultima_data(info["link"])
                if _ == 0:
                    d.adaugare_date({"link": info["link"], "pret": info["pret"]["nou"]})
                else:
                    if db.comparare_data_actuala_cu_ultima(_) == 1:
                        d.adaugare_date({"link": info["link"], "pret": info["pret"]["nou"]})
                d.inchidere_conexiune()
