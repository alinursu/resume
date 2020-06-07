autor = "Ursu Alin"
import os
import sys

from scripts.scrapper import Scrapper
from scripts import utils
from scripts.CEL import cel_string
from scripts import db
from scripts.htmlcreator import creatorHTML, HTML_adaugare_regasire, creatorHTML_gift
from scripts.debug import Debug, Verificare_Debug, Logger

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
jsonfn = "cel.json"

html_part_link = {"Laptopuri":"laptop-laptopuri",
                  "Laptopuri Refubrished":"laptopuri-reconditionate,renew",
                  "Tablete":"tablete",
                  "Telefoane":"telefoane-mobile",
                  "Smartwatch-uri":"smartwatch",
                  "Boxe Portabile":"boxe-portabile",
                  "Baterii Externe":"baterii-externe",
                  "Drone":"drone",
                  "Televizoare":"televizoare-lcd-led",
                  "Camere Video Sport":"accesorii-camere-video-sport",
                  "Sisteme Audio":"sisteme-audio",
                  "Procesoare":"procesoare",
                  "Placi de Baza":"placi-de-baza",
                  "Placi Video":"placi-video",
                  "Hard Disk-uri":"hard-disk-uri",
                  "Solid State Drive-uri":"ssd-uri",
                  "Casti":"casti",
                  "Boxe":"boxe",
                  "Desktop-uri":"calculatoare-desktop",
                  "Frigidere":"frigidere-combine-frigorifice",
                  "Masini de Spalat Rufe":"masini-de-spalat-rufe",
                  "Aparate de Aer Conditionat":"aparate-de-aer-conditionat",
                  "Centrale Termice":"centrale-termice"}

def Cel(categorie, pagini, cautare="normala"):
    """
    Functie ce preia informatii depsre produsele aflate la reducere dintr-o anumita categorie, de pe un anumit numar
    de pagini, de pe site-ul Cel.
    :param categorie:
    :return:
    """
    log = Logger()
    debug = Verificare_Debug()
    if cautare == "normala":
        categorie = html_part_link[categorie]
        s = Scrapper(jsonfn, categorie, None)
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
    for i in range(1, pagini+1):
        if cautare == "normala":
            html = s.get_html_code(s.jsondata["link_pagina"].format(categorie, i))
        elif cautare == "personalizata":
            html = s.get_html_code(s.jsondata["link_personalizat_pagina"].format(categorie, i))
        # Preiau lista produselor
        container = ""
        for el in html.select(s.jsondata["box"]["tag"]):
            try:
                if el[s.jsondata["box"]["tip"]] == s.jsondata["box"]["termen"]:
                    container = el
                    break
            except:
                pass

        # Preiau produsele
        prod = []
        for el in container.select(s.jsondata["produs"]["tag"]):
            try:
                if el[s.jsondata["produs"]["tip"]] == s.jsondata["produs"]["termen"]:
                    # Verific daca produsul este la reducere
                    for e in el.select(s.jsondata["produs"]["promo"]["tag"]):
                        try:
                            if e[s.jsondata["produs"]["promo"]["tip"]] == s.jsondata["produs"]["promo"]["termen"]:
                                prod.append(el)
                                break
                        except:
                            pass
            except:
                pass

        # Preiau link-ul spre produs
        for p in prod:
            for el in p.select(s.jsondata["href"]["tag"]):
                try:
                    if el[s.jsondata["href"]["tip"]] == s.jsondata["href"]["termen"]:
                        hrefs.append(el[s.jsondata["href"]["arg"]])
                        break
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

        # Preiau noul pret, vechiul pret si discount-ul produsului
        _ = {}
        for el in html.select(s.jsondata["data"]["pret"]["nou"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["nou"]["tip"]] == s.jsondata["data"]["pret"]["nou"]["termen"]:
                    _["nou"] = el.text + " Lei"
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["pret"]["vechi"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["vechi"]["tip"]] == s.jsondata["data"]["pret"]["vechi"]["termen"]:
                    __ = el.text.split("|")[-1].split(" ")
                    _["vechi"] = __[-2] + " " + __[-1].capitalize()
                    __ = el.text.split("|")[0].split(" ")
                    _["discount"] = __[-3] + " " + __[-2].capitalize()
            except:
                pass
        info["pret"] = _

        # Preiau rating-ul produsului (Daca exista. Daca nu, se initializeaza cu 0 automat)
        _ = {}
        ok = 0
        for el in html.select(s.jsondata["data"]["rating"]["rata"]["tag"]):
            try:
                if el[s.jsondata["data"]["rating"]["rata"]["tip"]] == s.jsondata["data"]["rating"]["rata"]["termen"]:
                    _["rata"] = el.text
                    ok = 1
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
        if ok == 1:
            info["rating"] = _
        elif ok == 0:
            info["rating"] = {"rata":"0", "review-uri":"0"}

        # Preiau descrierea produsului
        _ = ""
        for el in html.select(s.jsondata["data"]["descriere"]["tag"]):
            try:
                if el[s.jsondata["data"]["descriere"]["tip"]] == s.jsondata["data"]["descriere"]["termen"]:
                    _ = cel_string.formare_descriere(el.text)
                    break
            except:
                pass
        if _ != "" and _ != []:
            info["descriere"] = _
        else:
            info["descriere"] = ['']

        # Preiau specificatiile produsului
        _ = {}
        for el in html.select(s.jsondata["data"]["specs"]["tag"]):
            try:
                if el[s.jsondata["data"]["specs"]["tip"]] == s.jsondata["data"]["specs"]["termen"]:
                    title = ""
                    __ = {}
                    for e in el.select(s.jsondata["data"]["specs"]["elem"]["tag"]):
                        try:
                            if len(e[s.jsondata["data"]["specs"]["elem"]["tip"]]) > 0:
                                e2 = e.select(s.jsondata["data"]["specs"]["elem"]["spec"]["tag"])
                                __[e2[0].text] = e2[1].text
                        except:
                            if title == "":
                                title = e.text
                            if len(__.keys()) > 0:
                                _[title] = __
                                __ = {}
                                title = e.text
                    if title != '':
                        _[title] = __
                    else:
                        _["Specs"] = __
            except:
                pass
        info["specs"] = cel_string.formare_specificatii(_)

        # Verific daca exista cadou si, daca da, preiau informatiile
        _ = {}
        gift = 0
        for el in html.select(s.jsondata["data"]["cadou"]["tag"]):
            try:
                if el[s.jsondata["data"]["cadou"]["tip"]] == s.jsondata["data"]["cadou"]["termen"]:
                    if debug == True:
                        Debug("Gift gasit!", 0)
                    gift = 1
                    t = ''
                    for e in el.select(s.jsondata["data"]["cadou"]["titlu"]["tag"]):
                        try:
                            if e[s.jsondata["data"]["cadou"]["titlu"]["tip"]] == s.jsondata["data"]["cadou"]["titlu"]["termen"]:
                                t = e.text
                                break
                        except:
                            pass
                    if t != '' :
                        _["titlu"] = t
                        for e in el.select(s.jsondata["data"]["cadou"]["pret"]["tag"]):
                            try:
                                if e[s.jsondata["data"]["cadou"]["pret"]["tip"]] == s.jsondata["data"]["cadou"]["pret"]["termen"]:
                                    _["pret"] = e.text
                                    break
                            except:
                                pass
                    else:
                        # Cadou fara pret, difera class-ul
                        for e in el.select(s.jsondata["data"]["cadou"]["titlu_farapret"]["tag"]):
                            try:
                                if e[s.jsondata["data"]["cadou"]["titlu_farapret"]["tip"]] == s.jsondata["data"]["cadou"]["titlu_farapret"]["termen"]:
                                    _["titlu"] = e.text
                            except:
                                pass
                        _["pret"] = "-"
                    __ = el.select(s.jsondata["data"]["cadou"]["link"]["tag"])
                    _["link"] = __[0][s.jsondata["data"]["cadou"]["link"]["arg"]]
                    gift_html = s.get_html_code(_["link"])
                    for e in gift_html.select(s.jsondata["data"]["cadou"]["imagine"]["tag"]):
                        try:
                            if e[s.jsondata["data"]["cadou"]["imagine"]["tip"]] == s.jsondata["data"]["cadou"]["imagine"]["termen"]:
                                for e2 in e.select(s.jsondata["data"]["cadou"]["imagine"]["tag2"]):
                                    try:
                                        _["imagine_link"] = cel_string.link_cadou_imagine(e2[s.jsondata["data"]["cadou"]["imagine"]["arg"]])
                                        break
                                    except:
                                        pass
                                break
                        except:
                            pass
                    break
            except:
                pass
        if gift == 1:
            info["cadou"] = _

        # Salvez link-ul spre produs
        info["link"] = href

        # Preiau imaginile produsului
        imgs = []
        c = ""
        for el in html.select(s.jsondata["data"]["imagini"]["tag"]):
            try:
                if el[s.jsondata["data"]["imagini"]["tip"]] == s.jsondata["data"]["imagini"]["termen"]:
                    c = el
                    break
            except:
                pass
        sec_link = ""
        try:
            for el in c.select(s.jsondata["data"]["imagini"]["secundare"]["link"]["tag"]):
                try:
                    sec_link = el[s.jsondata["data"]["imagini"]["secundare"]["link"]["arg"]]
                    break
                except:
                    pass
        except:
            pass
        if sec_link != href and sec_link != '':
            sec_html = s.get_html_code(sec_link)
            for el in sec_html.select(s.jsondata["data"]["imagini"]["secundare"]["tag"]):
                try:
                    if el[s.jsondata["data"]["imagini"]["secundare"]["tip"]] == s.jsondata["data"]["imagini"]["secundare"]["termen"]:
                        for e in el.select(s.jsondata["data"]["imagini"]["secundare"]["img_tag"]):
                            try:
                                imgs.append(e[s.jsondata["data"]["imagini"]["secundare"]["arg"]])
                            except:
                                pass
                except:
                    pass
        elif sec_link == href and sec_link != '':
            # Inseamna ca exista doar o poza, cea principala
            for el in html.select(s.jsondata["data"]["imagini"]["tag"]):
                try:
                    if el[s.jsondata["data"]["imagini"]["tip"]] == s.jsondata["data"]["imagini"]["termen"]:
                        for e in el.select(s.jsondata["data"]["imagini"]["img_tag"]):
                            imgs.append(e[s.jsondata["data"]["imagini"]["arg"]])
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
                    IMGS.append(imgname + str(i) + ".{}".format(imgs[i].split("/")[-1].split(".")[-1]))
            except:
                if debug == True:
                    Debug("Eroare download {}".format(str(imgs[i])), 2)
        info["imagini"] = IMGS

        # Verific daca exista cadou si, daca da, downloadez imaginea cadoului
        if "cadou" in info.keys():
            try:
                utils.download_imagine(info["cadou"]["imagine_link"], imgname + "CADOU")
                info["cadou"]["imagine"] = imgname + "CADOU" + ".{}".format(info["cadou"]["imagine_link"].split("/")[-1].split(".")[-1])
            except:
                pass

        # Verific daca exista toate datele si, daca da, creez fisierul HTML
        if debug == True:
            Debug(str(info.keys()), 0)
            Debug(str(info["pret"].keys()), 0)
            Debug(str(info["rating"].keys()), 0)
            try:
                Debug(str(info["cadou"].keys()), 0)
            except:
                pass
        kw = {"titlu": None, "pret": ["vechi", "nou", "discount"], "rating": ["rata", "review-uri"], "descriere": None,
              "specs": None, "imagini": None, "link": None}
        kw_gift = {"titlu": None, "pret": ["vechi", "nou", "discount"], "rating": ["rata", "review-uri"],
                   "descriere": None, "specs": None, "imagini": None, "link": None,
                   "cadou": ["titlu", "pret", "link", "imagine", "imagine_link"]}
        if "cadou" in info.keys():
            if utils.verificare_date(info, kw_gift) == False:
                # Daca nu sunt toate datele necesare, sterg pozele descarcate
                if debug == True:
                    Debug("Date insuficente!", 2)
                utils.stergere_set_imagini(imgname)
            else:
                log.scriere("Salvez fisierul HTML.")
                creatorHTML_gift(info)
                d = db.Database("cel")
                d.initializare_conexiune()
                x = d.cautare_date_link(info["link"])
                if len(x) == 0:
                    _ = d.cautare_ultima_data(info["link"])
                    if _ == 0:
                        d.adaugare_date_2({"link": info["link"], "pret": cel_string.transformare_pret_int(info["pret"]["nou"])})
                    else:
                        if db.comparare_data_actuala_cu_ultima(_) == 1:
                            d.adaugare_date_2({"link": info["link"], "pret": cel_string.transformare_pret_int(info["pret"]["nou"])})
                    d.inchidere_conexiune()
                else:
                    regasit = db.alegere_pretul_minim(x)
                    if regasit["pret"] < cel_string.transformare_pret_int(info["pret"]["nou"]):
                        if debug == True:
                            Debug("Produsul a fost regasit!", 0)
                        HTML_adaugare_regasire(info["titlu"], regasit["data"], regasit["pret"])
                    _ = d.cautare_ultima_data(info["link"])
                    if _ == 0:
                        d.adaugare_date_2({"link": info["link"], "pret": cel_string.transformare_pret_int(info["pret"]["nou"])})
                    else:
                        if db.comparare_data_actuala_cu_ultima(_) == 1:
                            d.adaugare_date_2({"link": info["link"], "pret": cel_string.transformare_pret_int(info["pret"]["nou"])})
                    d.inchidere_conexiune()


        else:
            if utils.verificare_date(info, kw) == False:
                # Daca nu sunt toate datele necesare, sterg pozele descarcate
                if debug == True:
                    Debug("Date insuficiente", 2)
                utils.stergere_set_imagini(imgname)
            else:
                log.scriere("Salvez fisierul HTML.")
                creatorHTML(info)
                d = db.Database("cel")
                d.initializare_conexiune()
                x = d.cautare_date_link(info["link"])
                if len(x) == 0:
                    _ = d.cautare_ultima_data(info["link"])
                    if _ == 0:
                        d.adaugare_date_2({"link": info["link"], "pret": cel_string.transformare_pret_int(info["pret"]["nou"])})
                    else:
                        if db.comparare_data_actuala_cu_ultima(_) == 1:
                            d.adaugare_date_2({"link": info["link"], "pret": cel_string.transformare_pret_int(info["pret"]["nou"])})
                    d.inchidere_conexiune()
                else:
                    regasit = db.alegere_pretul_minim(x)
                    if regasit["pret"] < cel_string.transformare_pret_int(info["pret"]["nou"]):
                        if debug == True:
                            Debug("Produsul a fost regasit!", 0)
                        HTML_adaugare_regasire(info["titlu"], regasit["data"], regasit["pret"])
                    _ = d.cautare_ultima_data(info["link"])
                    if _ == 0:
                        d.adaugare_date_2({"link": info["link"], "pret": cel_string.transformare_pret_int(info["pret"]["nou"])})
                    else:
                        if db.comparare_data_actuala_cu_ultima(_) == 1:
                            d.adaugare_date_2({"link": info["link"], "pret": cel_string.transformare_pret_int(info["pret"]["nou"])})
                    d.inchidere_conexiune()
