autor = "Ursu Alin"
import os
import sys

from scripts.scrapper import Scrapper
from scripts.ALTEX import altex_string
from scripts import utils
from scripts.htmlcreator import creatorHTML, HTML_adaugare_regasire
from scripts import db
from scripts.debug import Debug, Verificare_Debug, Logger

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
jsonfile = "altex.json"

html_part_link = {"Telefoane":"telefoane",
                  "Smartwatch":"smartwatches",
                  "Boxe portabile":"boxe-portabile-telefoane-tablete",
                  "Casti":"casti-telefon",
                  "Tablete":"tablete",
                  "Laptopuri":"laptopuri",
                  "Sisteme PC":"sisteme-pc-calculatoare",
                  "Hard Disk-uri":"hard-disk-drive-hdd",
                  "Solid State Drive-uri":"solid-state-drive-ssd",
                  "Placi Video":"placi-video-calculator",
                  "Placi de Baza":"placi-baza-calculator",
                  "Procesoare":"procesoare-calculator",
                  "Memorii RAM":"memorii-calculator",
                  "Surse de Alimentare":"surse-alimentare-calculator",
                  "Carcase":"carcase-calculator",
                  "HDD Extern":"hdd-ssd-externe",
                  "Memorii USB":"memorii-usb",
                  "Boxe Calculator":"boxe-periferice-accesorii-it",
                  "Imprimante":"imprimante",
                  "Console PlayStation 4":"console-ps4",
                  "Console Xbox One":"console-xbox-one",
                  "Jocuri PC":"jocuri-pc",
                  "Televizoare":"televizoare",
                  "Sisteme Audio":"sisteme-audio",
                  "Soundbar si Home Cinema":"soundbar-home-cinema",
                  "Videoproiectoare":"videoproiectoare",
                  "Aer Conditionat":"aer-conditionat",
                  "Masini de Spalat Rufe":"masini-spalat-rufe",
                  "Frigidere":"frigidere",
                  "Masini de Spalat Vase":"masini-spalat-vase-electrocasnice",
                  "Expresoare Cafea":"expresoare-cafea"}

def Altex(categorie, suma_maxima, pagini, cautare="normala"):
    """
        Functie ce preia informatii despre produsele aflate la reducere dintr-o anumita categorie, pana intr-o anumita
        suma, de pe un anumit numar de pagini, de pe site-ul Altex.
        :param categorie:
        :param suma_maxima:
        :return:
        """
    log = Logger()
    debug = Verificare_Debug()
    if suma_maxima == None:
        suma_maxima = 999999
    if cautare == "normala":
        categorie = html_part_link[categorie]
        s = Scrapper(jsonfile, categorie, suma_maxima)
    elif cautare == "personalizata":
        s = Scrapper(jsonfile, categorie, suma_maxima, cautare="personalizata")

    html = s.get_html_code(s.link)
    log.scriere("Preiau date de pe {}.".format(s.link))
    print(s.link)

    # Preiau numarul maxim de pagini
    pagini_max = ""
    for el in html.select(s.jsondata["pagini"]["tag"]):
        try:
            if el[s.jsondata["pagini"]["tip"]] == s.jsondata["pagini"]["termen"]:
                script = el
        except:
            pass
    for el in script.select(s.jsondata["pagini"]["pagina"]["tag"]):
        try:
            if el[s.jsondata["pagini"]["pagina"]["tip"]] == s.jsondata["pagini"]["pagina"]["termen"]:
                pagini_max = int(el.text.split("/")[1])
                break
        except:
            pass

    #  Setez numarul de pagini de pe care se vor prelua produse, comparand datele introduse de utilizator cu numarul
    # maxim de pagini admis de cautare
    if pagini == None:
        pagini = 10
    if pagini > pagini_max:
        pagini = pagini_max

    # Pentru fiecare pagina in parte
    hrefs = []
    for pag in range(1, pagini+1):
        if cautare == "normala":
            html = s.get_html_code(s.jsondata["link_pagina"].format(categorie, suma_maxima, pag))
        elif cautare == "personalizata":
            html = s.get_html_code(s.jsondata["link_personalizat_pagina"].format(suma_maxima, pag, categorie))
        # Preiau lista produselor
        prod = []
        for el in html.select(s.jsondata["item"]["tag"]):
            try:
                if el[s.jsondata["item"]["tip"]] == s.jsondata["item"]["termen"]:
                    prod.append(el)
            except:
                pass

        # Preiau link-urile spre produs
        for p in prod:
            for el in p.select(s.jsondata["item_link"]["tag"]):
                try:
                    for e in el.select(s.jsondata["item_link"]["link"]["tag"]):
                        hrefs.append(e[s.jsondata["item_link"]["link"]["arg"]])
                        break
                    break
                except:
                    pass

    # Preiau informatiile fiecarui produs
    for href in hrefs:
        print(href)
        log.scriere("Preiau informatiile de pe {}.".format(href))
        if debug == True:
            Debug(href, 0)
        html = s.get_html_code(href)
        info = {}

        # Preiau titlul produsului
        for el in html.select(s.jsondata["data"]["titlu"]["tag"]):
            try:
                if el[s.jsondata["data"]["titlu"]["tip"]] == s.jsondata["data"]["titlu"]["termen"]:
                    info["titlu"] = el.text
                    break
            except:
                pass

        # Preiau pretul, pretul vechi si discount-ul produsului
        _ = {}
        for el in html.select(s.jsondata["data"]["pret"]["nou"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["nou"]["tip"]] == s.jsondata["data"]["pret"]["nou"]["termen"]:
                    _["nou"] = altex_string.formare_pret_nou(el.text)
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["pret"]["vechi"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["vechi"]["tip"]] == s.jsondata["data"]["pret"]["vechi"]["termen"]:
                    _["vechi"] = altex_string.formare_pret_vechi(el.text)
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["pret"]["discount"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["discount"]["tip"]] == s.jsondata["data"]["pret"]["discount"]["termen"]:
                    _["discount"] = altex_string.formare_pret_reducere(el.text)
                    break
            except:
                pass
        info["pret"] = _

        # Preiau rating-ul si numarul de review-uri ale produsului
        _ = {}
        for el in html.select(s.jsondata["data"]["rating"]["rata"]["tag"]):
            try:
                if el[s.jsondata["data"]["rating"]["rata"]["tip"]] == s.jsondata["data"]["rating"]["rata"]["termen"]:
                    _["rata"] = el.text.split(" ")[0]
                    break
            except:
                pass
        __ = ""
        for el in html.select(s.jsondata["data"]["rating"]["review-uri"]["tag"]):
            try:
                if el[s.jsondata["data"]["rating"]["review-uri"]["tip"]] == s.jsondata["data"]["rating"]["review-uri"]["termen"]:
                    __ = el.text
                    break
            except:
                pass
        if __ == "":
            _["review-uri"] = "0"
        else:
            _["review-uri"] = __
        info["rating"] = _

        # Preiau descrierea produsului
        desc = ""
        for el in html.select(s.jsondata["data"]["descriere"]["tag"]):
            try:
                if el[s.jsondata["data"]["descriere"]["tip"]] == s.jsondata["data"]["descriere"]["termen"]:
                    desc = altex_string.formare_descriere(el.text)
                    break
            except:
                pass
        if desc != "":
            if altex_string.verificare_functie_initFlix(desc) == 0:
                info["descriere"] = desc
            else:
                desc = altex_string.stergere_functie_initFlix(desc)
                info["descriere"] = desc

        # Preiau specificatiile produsului
        container = ""
        for el in html.select(s.jsondata["data"]["specs"]["container"]["tag"]):
            try:
                if el[s.jsondata["data"]["specs"]["container"]["tip"]] == s.jsondata["data"]["specs"]["container"]["termen"]:
                    container = el
                    break
            except:
                pass
        titles = []
        try:
            for el in container.select(s.jsondata["data"]["specs"]["titlu"]["tag"]):
                try:
                    if el[s.jsondata["data"]["specs"]["titlu"]["tip"]] == s.jsondata["data"]["specs"]["titlu"]["termen"]:
                        titles.append(el.text)
                except:
                    pass
            n = 0
            specs = {}
            for el in container.select(s.jsondata["data"]["specs"]["tabla"]["tag"]):
                try:
                    if el[s.jsondata["data"]["specs"]["tabla"]["tip"]] == s.jsondata["data"]["specs"]["tabla"]["termen"]:
                        _ = {}
                        k = ""
                        for e in el.select(s.jsondata["data"]["specs"]["tabla"]["info"]["tag"]):
                            try:
                                if e[s.jsondata["data"]["specs"]["tabla"]["info"]["tip"]] == s.jsondata["data"]["specs"]["tabla"]["info"]["termen"]:
                                    if k == "":
                                        k = e.text
                                    else:
                                        _[k] = e.text
                                        k = ""
                            except:
                                pass
                        specs[titles[n]] = _
                        n = n + 1
                except:
                    pass
        except:
            pass
        try:
            info["specs"] = specs
        except:
            pass

        # Salvez link-ul spre produs
        info["link"] = href

        # Preiau imaginile produsului
        imgs = []
        for el in html.select(s.jsondata["data"]["imagini"]["matrice"]["tag"]):
            try:
                if el[s.jsondata["data"]["imagini"]["matrice"]["tip"]] == s.jsondata["data"]["imagini"]["matrice"]["termen"]:
                    for e in el.select(s.jsondata["data"]["imagini"]["matrice"]["tag2"]):
                        matrice = altex_string.formare_matrice(e[s.jsondata["data"]["imagini"]["matrice"]["arg"]])
                        break
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["imagini"]["tag"]):
            try:
                if el[s.jsondata["data"]["imagini"]["tip"]] == s.jsondata["data"]["imagini"]["termen"]:
                    for e in el.select(s.jsondata["data"]["imagini"]["tag2"]):
                        _ = e[s.jsondata["data"]["imagini"]["arg"]]
                        imgs.append(matrice.format(_.split("/")[-1]))
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
                if utils.verificare_prezenta_imagine(imgname + str(i)) == True:
                    IMGS.append(imgname + str(i) + ".{}".format(imgs[i].split("/")[-1].split(".")[1]))
            except:
                if debug == True:
                    Debug("Eroare download {}".format(str(imgs[i])), 2)
        if len(IMGS) > 0:
            info["imagini"] = IMGS

        # Verific daca exista toate datele si, daca da, creez fisierul HTML
        print(info.keys())
        print(info["pret"].keys())
        print(info["rating"].keys())
        if debug == True:
            Debug(str(info.keys()), 0)
            Debug(str(info["pret"].keys()), 0)
            Debug(str(info["rating"].keys()), 0)
        kw = {"titlu": None, "pret": ["vechi", "nou", "discount"], "rating": ["rata", "review-uri"], "descriere": None,
              "specs": None, "imagini": None, "link": None}
        if utils.verificare_date(info, kw) == False:
            # Daca nu sunt toate datele necesare, sterg pozele descarcate
            if debug == True:
                Debug("Date insuficiente!", 2)
            utils.stergere_set_imagini(imgname)

        else:
            log.scriere("Salvez fisierul HTML.")
            creatorHTML(info)
            d = db.Database("altex")
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
