autor = "Ursu Alin"
import os
import sys

from scripts import utils
from scripts.scrapper import Scrapper
from scripts.LAVAS import lavas_string
from scripts.htmlcreator import creatorHTML_nautics, HTML_adaugare_regasire
from scripts import db
from scripts.debug import Debug, Verificare_Debug, Logger

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
jsonfile = "lavas.json"

def Lavas():
    """
    Functie ce preia informatii despre produsele aflate la reducere de pe site-ul Lavas.
    :return:
    """
    log = Logger()
    debug = Verificare_Debug()
    s = Scrapper(jsonfile, None, None)
    log.scriere("Preiau date de pe {}.".format(s.link))
    html = s.get_html_code(s.link)

    # Preiau lista produselor
    for el in html.select(s.jsondata["container"]["tag"]):
        try:
            if el[s.jsondata["container"]["tip"]] == s.jsondata["container"]["termen"]:
                container = el
                break
        except:
            pass

    # Preiau link-urile spre produse
    hrefs = []
    for el in container.select(s.jsondata["produs"]["tag"]):
        try:
            if el[s.jsondata["produs"]["tip"]] == s.jsondata["produs"]["termen"]:
                # Nu mai verific daca produsele se afla la reducere pentru ca au fost aplicate deja filtre
                hrefs.append(el[s.jsondata["produs"]["arg"]])
        except:
            pass

    # Preiau informatiile de la fiecare produs
    for href in hrefs:
        log.scriere("Preiau informatiile de pe {}.".format(s.jsondata["produs_link"].format(href)))
        if debug == True:
            Debug(href, 0)
        info = {}
        html = s.get_html_code(s.jsondata["produs_link"].format(href))

        # Preiau titlul produsului
        for el in html.select(s.jsondata["data"]["titlu"]["tag"]):
            try:
                if el[s.jsondata["data"]["titlu"]["tip"]] == s.jsondata["data"]["titlu"]["termen"]:
                    _ = lavas_string.formare_titlu(el.text)
                    try:
                        _ = lavas_string.modificare_nume_hashtag(_)
                    except:
                        pass
                    info["titlu"] = _
                    break
            except:
                pass

        # Preiau preturile si calculez discount-ul produsului
        _ = {}
        for el in html.select(s.jsondata["data"]["pret"]["nou"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["nou"]["tip"]] == s.jsondata["data"]["pret"]["nou"]["termen"]:
                    _["nou"] = lavas_string.formare_pret(el.text)
                    break
            except:
                pass
        for el in html.select(s.jsondata["data"]["pret"]["vechi"]["tag"]):
            try:
                if el[s.jsondata["data"]["pret"]["vechi"]["tip"]] == s.jsondata["data"]["pret"]["vechi"]["termen"]:
                    _["vechi"] = lavas_string.formare_pret(el.text)
                    break
            except:
                break
        _["discount"] = lavas_string.calculare_discount(_["nou"], _["vechi"])
        info["pret"] = _

        # Preiau descrierea produsului
        for el in html.select(s.jsondata["data"]["descriere"]["tag"]):
            try:
                if el[s.jsondata["data"]["descriere"]["tip"]] == s.jsondata["data"]["descriere"]["termen"]:
                    info["descriere"] = lavas_string.formare_descriere(el.text)
                    break
            except:
                pass

        # Salvez link-ul produsului
        info["link"] = s.jsondata["produs_link"].format(href)

        # Preiau imaginile produsului
        imgs = []
        for el in html.select(s.jsondata["data"]["imagine"]["tag"]):
            try:
                if el[s.jsondata["data"]["imagine"]["tip"]] == s.jsondata["data"]["imagine"]["termen"]:
                    _ = el[s.jsondata["data"]["imagine"]["arg"]]
                    imgs.append("https://" + _.split("//")[1])
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
        try:
            imgname = lavas_string.modificare_nume_hashtag(imgname)
        except:
            pass
        IMGS = []
        log.scriere("Descarc {} imagini.".format(len(imgs)))
        for i in range(0, len(imgs)):
            try:
                utils.download_imagine(imgs[i], imgname + str(i), extensie=imgs[i].split("/")[-1].split(".")[-1].split("?")[0])
                IMGS.append(imgname + str(i) + ".{}".format(imgs[i].split("/")[-1].split(".")[-1].split("?")[0]))
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
            # Daca nu sunt toate datele necesare, sterg imaginile produsului
            if debug == True:
                Debug("Date insuficiente!", 2)
            utils.stergere_set_imagini(imgname)
        else:
            log.scriere("Salvez fisierul HTML.")
            creatorHTML_nautics(info)
            d = db.Database("lavas")
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
