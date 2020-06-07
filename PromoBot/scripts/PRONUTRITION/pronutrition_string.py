autor = "Ursu Alin"
import os
import sys
import colorama

from scripts import utils

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
imagespath = path + "bin" + slash + "data" + slash + "images" + slash
htmlpath = path + "bin" + slash + "html" + slash
colorama.init()

def formare_pret(pret):
    """
    Functie ce preia un string ca si parametru, reprezentand pretul unui produs, si returneaza un alt string, diferit
    de cel inital prin faptul ca lipsesc anumite caractere ('\xa0').
    :param pret:
    :return:
    """
    pret = pret.split("\xa0")
    pret = pret[0] + ' ' + pret[1]
    return pret

def transformare_rating(rate):
    """
    Functie ce primeste un string ca si parametru, reprezentand rating-ul unui produs, aflat intr-un format procentual
    (0->100%), si returneaza un string echivalent, aflat intr-un format ce utilizeaza numarul de stele (0->5).
    :return:
    """
    rate = int(rate.split("%")[0])
    rate = rate / 10
    rate = str(rate/2)
    return rate

def formare_descriere(desc):
    """
    Functia primeste un string ca si parametru, reprezintand descrierea unui produs, si returneaza o lista de propozitii
    a descrierii, scapand si de spatiile de la inceputul si finalul fiecarei propoziiti.
    ex: '  Test prop1. Test prop2.   ' => ['Test prop1.", "Test prop2."]
    :param desc:
    :return:
    """
    desc = desc.split(".")
    _ = []
    for i in range(0, len(desc)):
        __ = desc[i].split()
        d = ""
        try:
            for j in range(0, len(__)-1):
                d = d + __[j] + " "
            d = d + __[-1] +"."
            _.append(d)
        except:
            pass
    return _

def preluare_img_link(script):
    """
    Functie primeste ca si parametru un string, reprezentand un cod javascript, si returneaza link-ul imaginii, acesta
    aflandu-se in interiorul script-ului.
    :param script:
    :return:
    """
    script = script.split("\n")
    _ = ""
    for line in script:
        __ = ""
        t = line.split()
        for cuv in t:
            __ = __ + cuv + " "
        _ = _ + __ + "\n"
    script = _
    code = ""
    for line in script.split("\n"):
        if '"data"' in line:
            code = line.split(": ")[1]
            break
    link = ""
    for el in code.split(","):
        if "full" in el:
            link = el.split(":")[1] + ":" + el.split(":")[2]
            break
    link = eval(link)
    link = link.split("\/")
    _ = ""
    for i in range(0, len(link)-1):
        _ = _ + link[i] + "/"
    _ = _ + link[-1]
    link = _
    return link