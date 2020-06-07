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

def formare_titlu(titlu):
    """
    Preia un string, reprezentand titlul unui produs, si scapa de anumite caractere.
    ex: '\nBratara Chakra ajustabila\n' => 'Bratara Chakra ajustabila'
    :param titlu:
    :return:
    """
    return titlu.split("\n")[1]

def formare_pret(pret):
    """
    Preia un string, reprezentand pretul unui produs, si scapa de anumite caractere.
    ex: '\n-\n42,00 lei\n' => '42,00 lei'
    :param pret:
    :return:
    """
    pret = pret.split("\n")
    ok = 0
    while ok == 0:
        ok = 1
        try:
            for i in range(0, len(pret)):
                if utils.verificare_string_gol(pret[i]) == True:
                    del pret[i]
                    ok = 0
        except:
            pass
    pret = pret[0]
    return pret

def calculare_discount(nou, vechi):
    """
    Functie ce preia doua string-uri ca si parametri, reprezentand pretul nou si pretul vechi al unui produs, si
    calculeaza discount-ul produsului, returnand valoarea intreaga in format string.
    ex: ('46,00 lei', '34,00 lei') =>
    :param nou:
    :param vechi:
    :return:
    """
    nou = int(nou.split(" ")[0].split(",")[0])
    vechi = int(vechi.split(" ")[0].split(",")[0])
    discount = abs(100 - int(nou*100/vechi) - 1)
    discount = "{}%".format(discount)
    return discount

def formare_descriere(desc):
    """
    Functie ce preia un string ca si parametru, reprezentand descrierea unui produs, si returneaza o lista ce contine
    cate o linie a descrierii unui produs, scapand de anumite caractere (ex: "\n", "\xa0").
    :param desc:
    :return:
    """
    desc = desc.split("\n")
    ok = 0
    while ok == 0:
        ok = 1
        try:
            for i in range(0, len(desc)):
                if utils.verificare_string_gol(desc[i]) == True:
                    del desc[i]
                    ok = 0
        except:
            pass
    for i in range(0, len(desc)):
        _ = desc[i].split("\xa0")
        __ = ""
        for j in range(0, len(_)):
            if utils.verificare_string_gol(_[j]) == False:
                __ = __ + _[j] + " "
        desc[i] = __
    return desc

def modificare_nume_hashtag(nume):
    """
    Functie ce modifica numele partial ale imaginilor unui obiect. Mai exact, scapa de caracterul '#' pentru ca provoaca
    o eroare in codul HTML.
    :param nume:
    :return:
    """
    _ = nume.split("#")
    nume = _[0] + _[1]
    return nume