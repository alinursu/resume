autor = "Ursu Alin"
import os
import sys

from scripts import utils
from scripts.scrapper import Scrapper
from scripts.CONSTANTINNAUTICS import nautics_string
from scripts.htmlcreator import creatorHTML_nautics, HTML_adaugare_regasire
from scripts import db
from scripts.debug import Debug, Verificare_Debug, Logger

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd()
jsonfile = "constantinnautics.json"

def ConstantinNautics():
    """
    Functie ce preia informatii despre produsele aflate la reducere de pe site-ul Constantin Nautics.
    :return:
    """
    log = Logger()
    debug = Verificare_Debug()
    s = Scrapper(jsonfile, None, None)
    html = s.get_html_code(s.link)
    log.scriere("Preiau date de pe {}.".format(s.link))

    # Preiau lista produselor
    container = ""
    for el in html.select(s.jsondata["container"]["tag"]):
        try:
            if el[s.jsondata["container"]["tip"]] == s.jsondata["container"]["termen"]:
                container = el
                break
        except:
            pass

    # Preiau produsele
    prod = []
    for el in container.select(s.jsondata["produs"]["tag"]):
        try:
            if el[s.jsondata["produs"]["tip"]] == s.jsondata["produs"]["termen"]:
                prod.append(el)
        except:
            pass

    # Preiau link-urile spre produse
    hrefs = []
    for p in prod:
        for el in p.select(s.jsondata["href"]["link_tag"]):
            try:
                hrefs.append(el[s.jsondata["href"]["arg"]])
                break
            except:
                pass

    # Preiau discount-urile fiecarui link pentru ca acestea apar doar in lista principala (si elimin minusul)
    discounts = {}
    i = -1
    for el in container.select(s.jsondata["produs"]["tag"]):
        try:
            if el[s.jsondata["produs"]["tip"]] == s.jsondata["produs"]["termen"]:
                i = i + 1
                # Nu mai verific daca produsele se afla la reducere pentru ca au fost aplicate deja filtre
                for e in el.select(s.jsondata["discount"]["tag"]):
                    try:
                        if e[s.jsondata["discount"]["tip"]] == s.jsondata["discount"]["termen"]:
                            discounts[hrefs[i]] = e.text.split("-")[1]
                            break
                    except:
                        pass
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
                    if '#' in el.text.split("\n")[1]:
                        info["titlu"] = nautics_string.formare_titlu(el.text.split("\n")[1])
                    else:
                        info["titlu"] = el.text.split("\n")[1]
                    break
            except:
                pass

        # Preiau pretul nou si pretul vechi ale produsului
        _ = {}
        for el in html.select(s.jsondata["data"]["pret"]["nou"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["nou"]["tip"]] == s.jsondata["data"]["pret"]["nou"]["termen"]:
                    _["nou"] = el.text
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["pret"]["vechi"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["vechi"]["tip"]] == s.jsondata["data"]["pret"]["vechi"]["termen"]:
                    _["vechi"] = el.text
                    break
            except:
                pass
        _["discount"] = discounts[href]
        info["pret"] = _

        # Preiau descrierea produsului
        for el in html.select(s.jsondata["data"]["descriere"]["tag"]):
            try:
                if el[s.jsondata["data"]["descriere"]["tip"]] == s.jsondata["data"]["descriere"]["termen"]:
                    info["descriere"] = nautics_string.formare_descriere(el.text)
                    break
            except:
                pass

        # Salvez link-ul spre produs
        info["link"] = href

        # Preiau imaginile produsului
        imgs = []
        for el in html.select(s.jsondata["data"]["imagine"]["tag"]):
            try:
                if el[s.jsondata["data"]["imagine"]["tip"]] == s.jsondata["data"]["imagine"]["termen"]:
                    for e in el.select(s.jsondata["data"]["imagine"]["img_tag"]):
                        try:
                            imgs.append(e[s.jsondata["data"]["imagine"]["arg"]])
                        except:
                            pass
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
        if '#' in imgname:
            imgname = nautics_string.modificare_nume_partial_imagini(imgname)
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
        kw = {"titlu": None, "pret": ["vechi", "nou", "discount"], "descriere": None, "imagini": None, "link": None}
        if utils.verificare_date(info, kw) == False:
            # Daca nu sunt toate datele necesare, sterg pozele descarcate
            if debug == True:
                Debug("Date insuficiente!", 2)
            utils.stergere_set_imagini(imgname)
        else:
            log.scriere("Salvez fisierul HTML.")
            creatorHTML_nautics(info)
            d = db.Database("constantinnautics")
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
