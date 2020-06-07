autor = "Ursu Alin"
import os
import sys

from scripts import utils
from scripts.scrapper import Scrapper
from scripts.PRONUTRITION import pronutrition_string
from scripts.htmlcreator import creatorHTML_pronutrition, HTML_adaugare_regasire
from scripts import db
from scripts.debug import Debug, Verificare_Debug, Logger

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
jsonfile = "pronutrition.json"

def ProNutrition(pagini):
    """
    Functie ce preia informatii despre produsele aflate la reducere de pe un anumit numar de pagini, de pe site-ul ProNutrition.
    :return:
    """
    log = Logger()
    debug = Verificare_Debug()
    s = Scrapper(jsonfile, None, None)
    html = s.get_html_code(s.link)
    log.scriere("Preiau date de pe {}.".format(s.link))

    # Preiau numarul maxim de pagini
    pagini_max = 0
    for el in html.select(s.jsondata["pagini"]["tag"]):
        try:
            if el[s.jsondata["pagini"]["tip"]] == s.jsondata["pagini"]["termen"]:
                for e in el.select(s.jsondata["pagini"]["tag2"]):
                    try:
                        if pagini_max < int(e.text): pagini_max = int(e.text)
                    except:
                        pass
                break
        except:
            pass
    #  Setez numarul de pagini de pe care se vor prelua produse, comparand datele introduse de utilizator cu numarul
    # maxim de pagini admis de cautare
    if pagini == None:
        pagini = pagini_max
    elif pagini > pagini_max:
        pagini = pagini_max

    # Pentru fiecare pagina in parte preiau produsele
    hrefs = []
    for i in range(1, pagini+1):
        html = s.get_html_code(s.jsondata["link_pagina"].format(i))
        # Preiau lista produselor
        for el in html.select(s.jsondata["container"]["tag"]):
            try:
                if el[s.jsondata["container"]["tip"]] == s.jsondata["container"]["termen"]:
                    container = el
                    break
            except:
                pass

        # Preiau link-urile spre produse
        for el in container.select(s.jsondata["produs"]["tag"]):
            try:
                if el[s.jsondata["produs"]["tip"]] == s.jsondata["produs"]["termen"]:
                    # Nu mai verific daca produsele se afla la reducere pentru ca au fost aplicate deja filtre
                    hrefs.append(el[s.jsondata["produs"]["arg"]])
            except:
                pass

    # Preiau informatiile fiecarui produs
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

        # Preiau preturile si discount-ul produsului
        _ = {}
        for el in html.select(s.jsondata["data"]["pret"]["nou"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["nou"]["tip"]] == s.jsondata["data"]["pret"]["nou"]["termen"]:
                    _["nou"] = pronutrition_string.formare_pret(el.text)
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["pret"]["vechi"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["vechi"]["tip"]] == s.jsondata["data"]["pret"]["vechi"]["termen"]:
                    for e in el.select(s.jsondata["data"]["pret"]["vechi"]["valoare_veche"]["tag"]):
                        try:
                            if e[s.jsondata["data"]["pret"]["vechi"]["valoare_veche"]["tip"]] == s.jsondata["data"]["pret"]["vechi"]["valoare_veche"]["termen"]:
                                _["vechi"] = pronutrition_string.formare_pret(e.text)
                                break
                        except:
                            pass
                    if "vechi" in _.keys():
                        break
            except:
                pass
        for el in html.select(s.jsondata["data"]["pret"]["discount"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["discount"]["tip"]] == s.jsondata["data"]["pret"]["discount"]["termen"]:
                    _["discount"] = el.text.split("-")[-1]
                    break
            except:
                pass

        info["pret"] = _

        # Preiau rating-ul si numarul de review-uri ale produsului
        _ = {}
        for el in html.select(s.jsondata["data"]["rating"]["rata"]["tag"]):
            try:
                if el[s.jsondata["data"]["rating"]["rata"]["tip"]] == s.jsondata["data"]["rating"]["rata"]["termen"]:
                    _["rata"] = pronutrition_string.transformare_rating(el[s.jsondata["data"]["rating"]["rata"]["arg"]])
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["rating"]["review-uri"]["tag"]):
            try:
                if el[s.jsondata["data"]["rating"]["review-uri"]["tip"]] == s.jsondata["data"]["rating"]["review-uri"]["termen"]:
                    _["review-uri"] = el.text
                    break
            except:
                pass
        if len(_) == 0:
            info["rating"] = {"rata":"0", "review-uri":"0"}
        else:
            info["rating"] = _

        # Preiau descrierea produsului (+ ingredientele si modul de administrare, pe care le adaug la descriere)
        _ = []
        for el in html.select(s.jsondata["data"]["descriere"]["tag"]):
            try:
                if el[s.jsondata["data"]["descriere"]["tip"]] == s.jsondata["data"]["descriere"]["termen"]:
                    _ = pronutrition_string.formare_descriere(el.text)
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["descriere"]["ingrediente"]["tag"]):
            try:
                if el[s.jsondata["data"]["descriere"]["ingrediente"]["tip"]] == s.jsondata["data"]["descriere"]["ingrediente"]["termen"]:
                    _.append(el.text)
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["descriere"]["mod_administrare"]["tag"]):
            try:
                if el[s.jsondata["data"]["descriere"]["mod_administrare"]["tip"]] == s.jsondata["data"]["descriere"]["mod_administrare"]["termen"]:
                    _.append(el.text)
                    break
            except:
                pass
        info["descriere"] = _

        # Preiau specificatiile produsului (valorile nutritionale)
        _ = {}
        __ = ""
        for el in html.select(s.jsondata["data"]["specs"]["tag"]):
            try:
                if el[s.jsondata["data"]["specs"]["tip"]] == s.jsondata["data"]["specs"]["termen"]:
                    # Preiau titlul specificatiilor
                    title = "{} - {}"
                    for e in el.select(s.jsondata["data"]["specs"]["titlu"]["tag"]):
                        if len(__) == 0:
                            __ = e.text
                        else:
                            title = title.format(__, e.text)
                            break
                    # Preiau setul de specificatii
                    ___ = {}
                    __ = ""
                    for e in el.select(s.jsondata["data"]["specs"]["tag2"]):
                        if len(__) == 0:
                            __ = e.text
                        else:
                            ___[__] = e.text
                            __ = ""
                    _[title] = ___
            except:
                pass
        info["specs"] = _

        # Salvez link-ul catre produs
        info["link"] = href

        # Preiau imaginile produsului
        imgs = []
        for el in html.select(s.jsondata["data"]["imagine"]["tag"]):
            try:
                if el[s.jsondata["data"]["imagine"]["tip"]] == s.jsondata["data"]["imagine"]["termen"]:
                    for e in el.select(s.jsondata["data"]["imagine"]["tag2"]):
                        imgs.append(pronutrition_string.preluare_img_link(e.text))
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
            Debug(str(info["rating"].keys()), 0)
            try:
                Debug(str(info["gift"].keys()), 0)
            except:
                pass
        kw = {"titlu":None, "pret":["nou", "vechi", "discount"], "rating":["rata", "review-uri"], "descriere":None, "specs": None, "imagini":None, "link":None}
        if utils.verificare_date(info, kw) == False:
            # Daca nu sunt toate datele necesare, sterg pozele produsului
            if debug == True:
                Debug("Date insuficiente!", 2)
            utils.stergere_set_imagini(imgname)
        else:
            log.scriere("Salvez fisierul HTML.")
            creatorHTML_pronutrition(info)
            d = db.Database("pronutrition")
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
