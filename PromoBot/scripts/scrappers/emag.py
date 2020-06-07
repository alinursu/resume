autor = "Ursu Alin"
import os
import time
import sys

from scripts.scrapper import Scrapper
from scripts import utils, db
from scripts.EMAG import emag_string
from scripts.htmlcreator import creatorHTML, creatorHTML_gift, HTML_adaugare_regasire
from scripts.debug import Debug, Verificare_Debug, Logger

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
jsonfile = "emag.json"

html_part_link = {"Laptopuri":"laptopuri",
                  "Genti Laptop":"genti-laptop",
                  "Desktop PC":"desktop-pc",
                  "Placi Video":"placi_video",
                  "Procesoare":"procesoare",
                  "Placi de baza":"placi_baza",
                  "Solid-State Drive":"solid-state_drive_ssd_",
                  "Hard Disk-uri":"hard_disk-uri",
                  "Memorii":"memorii",
                  "Mouse":"mouse",
                  "Tastaturi":"tastaturi",
                  "Boxe PC":"boxe-pc",
                  "Casti PC":"casti-pc",
                  "Carcase PC":"carcase",
                  "Surse PC":"surse-pc",
                  "Memorii USB":"memorii-usb",
                  "Tablete Grafice":"tablete-grafice",
                  "Console Gaming":"console-hardware",
                  "Frigidere":"frigidere",
                  "Jocuri PC":"jocuri-consola-pc",
                  "Telefoane Mobile":"telefoane-mobile",
                  "Tablete":"tablete",
                  "Accesorii Tablete":"tablete-accesorii",
                  "Imprimante Laser":"imprimante-laser",
                  "Imprimante Inkjet":"imprimante-inkjet",
                  "Smartwatch":"smartwatch",
                  "Bratari Fitness":"bratari-fitness",
                  "Boxe HI-FI":"boxe",
                  "Boxe Portabile":"boxe-portabile",
                  "Casti Audio":"casti-audio",
                  "Aparate Foto DSLR":"aparate_foto_d-slr",
                  "Televizoare": "televizoare",
                  "Aragazuri":"aragazuri",
                  "Cuptoare cu Microunde":"cuptoare-cu-microunde",
                  "Espressor":"espressor",
                  "Aspiratoare":"aspiratoare",
                  "Aparate Aer-Conditionat":"aparate_aer_conditionat",
                  "Centrale Termice":"centrale-termice",
                  "Masini de Spalat Rufe":"masini-spalat-rufe",
                  "Masini de Spalat Vase":"masini-spalat-vase-standard",
                  "Genti Dame":"genti-dama",
                  "Rucsacuri Dame":"rucsacuri-dama",
                  "Ceasuri Dame":"ceasuri-dama",
                  "Genti Barbati":"genti-barbati",
                  "Rucsacuri Barbati":"rucsacuri-barbati",
                  "Ceasuri Barbati":"ceasuri-barbatesti"}

def Emag(categorie, suma_maxima, pagini, cautare="normala"):
    """
    Functie ce preia informatii despre produsele aflate la reducere dintr-o anumita categorie, pana intr-o anumita
        suma, de pe un anumit numar de pagini, de pe site-ul Emag.
    :param categorie:
    :param suma_maxima:
    :return:
    """
    log = Logger()
    debug = Verificare_Debug()
    if cautare == "normala":
        categorie = html_part_link[categorie]
        if suma_maxima == None:
            suma_maxima = 999999
        s = Scrapper(jsonfile, categorie, suma_maxima)
    elif cautare == "personalizata":
        s = Scrapper(jsonfile, categorie, None, cautare="personalizata")
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
        pagini = 10
    if pagini > pagini_max:
        pagini = pagini_max

    # Pentru fiecare pagina
    hrefs = []
    for i in range(1, pagini+1):
        if cautare == "normala":
            html = s.get_html_code(s.jsondata["link_pagina"].format(categorie, suma_maxima, i))
        elif cautare == "personalizata":
            html = s.get_html_code(s.jsondata["link_personalizat_pagina"].format(categorie, i))
        # Preiau produsele
        prod = []
        for el in html.select(s.jsondata["box"]["tag"]):
            try:
                if el[s.jsondata["box"]["tip"]] == s.jsondata["box"]["termen"]:
                    # Verific daca produsul este la reducere
                    for e in el.select(s.jsondata["detectare_reducere"]["tag"]):
                        try:
                            if e[s.jsondata["detectare_reducere"]["tip"]] == s.jsondata["detectare_reducere"]["termen"]:
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
                        hrefs.append(el["href"])
                        break
                except:
                    pass

    # Preiau informatiile fiecarui produs
    for href in hrefs:
        log.scriere("Preiau informatiile de pe {}.".format(href))
        if debug == True:
            Debug(href, 0)
        info = {}
        try:
            html = s.get_html_code(href)
        except:
            time.sleep(1)
            try:
                html = s.get_html_code(href)
            except:
                continue

        # Preiau titlul produsului
        for el in html.select(s.jsondata["data"]["titlu"]["tag"]):
            try:
                if el[s.jsondata["data"]["titlu"]["tip"]] == s.jsondata["data"]["titlu"]["termen"]:
                    info["titlu"] = emag_string.reparator_string(el.text, 1)
                    break
            except:
                pass

        # Preiau pretul, pretul vechi si discount-ul(%) produsului
        t = {}
        for el in html.select(s.jsondata["data"]["pret"]["nou"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["nou"]["tip"]] == s.jsondata["data"]["pret"]["nou"]["termen"]:
                    _ = emag_string.reparator_string(el.text, 4).split(" ")
                    __ = ""
                    for i in range(0, len(_[0])-2):
                        __ = __ + _[0][i]
                    __ = __ + ','
                    for i in range(len(_[0])-1, len(_[0])):
                        __ = __ + _[0][i]
                    __ = __ + ' ' + _[1]
                    t["nou"] = __
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["pret"]["vechi"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["vechi"]["tip"]] == s.jsondata["data"]["pret"]["vechi"]["termen"]:
                    _ = emag_string.reparator_string(el.text, 1).split(" ")
                    __ = ""
                    for i in range(0, len(_[0]) - 2):
                        __ = __ + _[0][i]
                    __ = __ + ','
                    for i in range(len(_[0]) - 1, len(_[0])):
                        __ = __ + _[0][i]
                    __ = __ + ' ' + _[1]
                    t["vechi"] = __

                    ___ = emag_string.reparator_string(el.text, 3)
                    if "%" in ___:
                        t["discount"] = ___
                    else:
                        t["discount"] = emag_string.formare_discount_lei(___)
                    break
            except:
                pass
        info["pret"] = t

        # Preiau rating-ul si numarul de review-uri ale produsului
        t = {}
        for el in html.select(s.jsondata["data"]["rating"]["rata"]["tag"]):
            try:
                if el[s.jsondata["data"]["rating"]["rata"]["tip"]] == s.jsondata["data"]["rating"]["rata"]["termen"]:
                    t["rata"] = emag_string.reparator_string(el.text, 1)
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["rating"]["review-uri"]["tag"]):
            try:
                if el[s.jsondata["data"]["rating"]["review-uri"]["tip"]] == s.jsondata["data"]["rating"]["review-uri"]["termen"]:
                    t["review-uri"] = emag_string.reparator_string(el.text, 1).split(" ")[0]
            except:
                pass
        if len(t) == 0:
            info["rating"] = {"rata":"0", "review-uri":"0"}
        else:
            info["rating"] = t

        # Preiau descrierea produsului
        for el in html.select(s.jsondata["data"]["descriere"]["tag"]):
            try:
                if el[s.jsondata["data"]["descriere"]["tip"]] == s.jsondata["data"]["descriere"]["termen"]:
                    info["descriere"] = emag_string.reparator_string_descriere(el.text)
            except:
                pass

        # Preiau specificatiile produsului
        _ = []
        for el in html.select(s.jsondata["data"]["specs"]["tag"]):
            try:
                if el[s.jsondata["data"]["specs"]["tip"]] == s.jsondata["data"]["specs"]["termen"]:
                    _.append(el)
            except:
                pass
        try:
            tmp = _[1]
        except:
            tmp = _[0]
        boxes = []
        for el in tmp.select(s.jsondata["data"]["specs"]["box"]["tag"]):
            try:
                if el[s.jsondata["data"]["specs"]["box"]["tip"]] == s.jsondata["data"]["specs"]["box"]["termen"]:
                    boxes.append(el)
            except:
                pass
        _ = {}
        for box in boxes:
            __ = {}
            t1 = []
            t2 = []
            # Titlul setului de specificatii
            for el in box.select(s.jsondata["data"]["specs"]["box"]["titlu"]["tag"]):
                try:
                    if el[s.jsondata["data"]["specs"]["box"]["titlu"]["tip"]] == s.jsondata["data"]["specs"]["box"]["titlu"]["termen"]:
                        title = el.text
                except:
                    pass
            # Preiau setul de specificatii
            for el in box.select(s.jsondata["data"]["specs"]["box"]["spec_titlu"]["tag"]):
                try:
                    if el[s.jsondata["data"]["specs"]["box"]["spec_titlu"]["tip"]] == s.jsondata["data"]["specs"]["box"]["spec_titlu"]["termen"]:
                        t1.append(el.text)
                except:
                    pass
            for el in box.select(s.jsondata["data"]["specs"]["box"]["spec_info"]["tag"]):
                try:
                    if el[s.jsondata["data"]["specs"]["box"]["spec_info"]["tip"]] == s.jsondata["data"]["specs"]["box"]["spec_info"]["termen"]:
                        t2.append(el.text)
                except:
                    pass
            # Creez setul de specificatii
            for i in range(0, len(t1)):
                __[t1[i]] = t2[i]
            _[title] = __
        info["specs"] = _

        # Verific daca exista cadou si, daca da, preiau informatiile
        for el in html.select(s.jsondata["data"]["cadou"]["tag"]):
            try:
                gift = {}
                if el[s.jsondata["data"]["cadou"]["tip"]] == s.jsondata["data"]["cadou"]["termen"]:
                    for e in el.select(s.jsondata["data"]["cadou"]["text"]["tag"]):
                        try:
                            if e[s.jsondata["data"]["cadou"]["text"]["tip"]] == s.jsondata["data"]["cadou"]["text"]["termen"]:
                                gift["titlu"] = e.text
                                break
                        except:
                            pass
                    for e in el.select(s.jsondata["data"]["cadou"]["pret"]["tag"]):
                        try:
                            if e[s.jsondata["data"]["cadou"]["pret"]["tip"]] == s.jsondata["data"]["cadou"]["pret"]["termen"]:
                                gift["pret"] = emag_string.formare_discount_lei(e.text.split("(")[1].split(")")[0])
                                break
                        except:
                            pass
                    for e in el.select(s.jsondata["data"]["cadou"]["link"]["tag"]):
                        try:
                            if e[s.jsondata["data"]["cadou"]["link"]["tip"]] == s.jsondata["data"]["cadou"]["link"]["termen"]:
                                for ee in e.select(s.jsondata["data"]["cadou"]["link"]["href"]["tag"]):
                                    gift["link"] = "https://emag.ro" + ee[s.jsondata["data"]["cadou"]["link"]["href"]["arg"]]
                                    break
                        except:
                            pass
                    for e in el.select(s.jsondata["data"]["cadou"]["imagine"]["tag"]):
                        try:
                            gift["imagine_link"] = e[s.jsondata["data"]["cadou"]["imagine"]["arg"]]
                        except:
                            pass
                    if len(gift.keys()) > 0:
                        info["cadou"] = gift
                    break
            except:
                pass

        # Preiau imaginile produsului
        imgs = []
        for el in html.select(s.jsondata["data"]["imagine"]["tag"]):
            try:
                if el[s.jsondata["data"]["imagine"]["tip"]] == s.jsondata["data"]["imagine"]["termen"]:
                    imgs.append(el[s.jsondata["data"]["imagine"]["link"]])
            except:
                pass
        # Descarc imaginile produsului
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
        imgname = emag_string.reparator_nume_imagini(imgname)
        IMGS = []
        log.scriere("Descarc {} imagini.".format(len(imgs)))
        for i in range(0, len(imgs)):
            try:
                utils.download_imagine(imgs[i], imgname + str(i))
                if utils.verificare_prezenta_imagine(imgname + str(i)) == True:
                    IMGS.append(imgname + str(i) + ".{}".format(imgs[i].split("/")[7].split(".")[1]))
            except:
                if debug == True:
                    Debug("Eroare download {}".format(str(imgs[i])), 2)
        if len(IMGS) > 0:
            info["imagini"] = IMGS

        # Daca exista cadou, descarc imaginea produsului
        if "cadou" in info.keys():
            if debug == True:
                Debug("Gift gasit!", 0)
            try:
                utils.download_imagine(info["cadou"]["imagine_link"], imgname + "CADOU")
                info["cadou"]["imagine"] = imgname + "CADOU" + ".{}".format(info["cadou"]["imagine_link"].split("/")[7].split(".")[1])
            except:
                pass

        # Salvez link-ul spre produs
        info["link"] = href

        # Verific daca exista toate datele si, daca da, creez fisierul HTML
        if debug == True:
            Debug(str(info.keys()), 0)
            Debug(str(info["pret"].keys()), 0)
            Debug(str(info["rating"].keys()), 0)
            try:
                Debug(str(info["cadou"].keys()), 0)
            except:
                pass
        kw = {"titlu":None, "pret":["vechi", "nou", "discount"], "rating":["rata", "review-uri"], "descriere":None, "specs": None, "imagini":None, "link":None}
        kw_gift = {"titlu": None, "pret": ["vechi", "nou", "discount"], "rating": ["rata", "review-uri"], "descriere": None, "specs": None, "imagini": None, "link": None, "cadou":["titlu", "pret", "link", "imagine", "imagine_link"]}

        if "cadou" in info.keys():
            if utils.verificare_date(info, kw_gift) == False:
                # Daca nu sunt toate datele necesare, sterg pozele produsului
                if debug == True:
                    Debug("Date insuficiente!", 2)
                utils.stergere_set_imagini(imgname)
            else:
                log.scriere("Salvez fisierul HTML.")
                creatorHTML_gift(info)
                d = db.Database("emag")
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


        else:
            if utils.verificare_date(info, kw) == False:
                # Daca nu exista toate datele necesare, sterg pozele produsului
                if debug == True:
                    Debug("Date insuficiente!", 2)
                utils.stergere_set_imagini(imgname)
            else:
                log.scriere("Salvez fisierul HTML.")
                creatorHTML(info)
                d = db.Database("emag")
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
