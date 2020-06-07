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

def reparator_string(string, pozitie_split):
    """
    Functie ce "repara" o valoare de tip STRING.
    ex: "        \nTEST\n          " => "TEST"
    :param string:
    :param pozitie_split:
    :return:
    """
    if pozitie_split != None:
        t = string.split("\n")[pozitie_split]
    else:
        t = string

    _ = []
    for char in t:
        _.append(char)
    while _[0] == ' ':
        del _[0]
    while _[len(_)-1] == ' ':
        del _[len(_)-1]

    t = ""
    for char in _:
        t = t + char
    return t

def reparator_string_descriere(t):
    """
    Functie folosita pentru a "repara" un text mai mare (cum ar fi cel dintr-o descriere), pe care il si imparte intr-o
    lista de propozitii mai mici.
    :param t:
    :return:
    """
    t = t.split("\t")

    ok = 0
    while ok == 0:
        ok = 1
        for i in range(0, len(t)):
            try:
                if t[i] == "" or t[i] == "\n" or t[i] == " \n":
                    ok = 0
                    del t[i]
            except:
                break

    for i in range(0, len(t)):
        _ = t[i].split("\n")
        for __ in _:
            if __ != ' ' and __ != '':
                t[i] = __

    for i in range(0, len(t)):
        try:
            t[i] = reparator_string(t[i], None)
        except:
            pass

    ok = 0
    while ok == 0:
        ok = 1
        for i in range(0, len(t)):
            try:
                if "\n" in t[i]:
                    del t[i]
                    ok = 0
            except:
                break

    ok = 0
    while ok == 0:
        ok = 1
        for i in range(0, len(t)):
            try:
                if utils.verificare_string_gol(t[i]) == True: #string-ul e gol
                    del t[i]
                    ok = 0
            except:
                break

    return t

def formare_discount_lei(discount):
    """
    Functie ce formeaza un string reprezentand discount-ul in lei deoarece lipseste virgula si apare confuzia.
    Exemplu: "5000 Lei" => "50,00 Lei"
    :param discount:
    :return:
    """
    _ = discount.split(" ")
    __ = []
    for char in _[0]:
        __.append(char)
    d = ""
    for i in range(0, len(__)-2):
        d = d + __[i]
    d = d + ","
    for i in range(len(__)-2, len(__)):
        d = d + __[i]
    d = d + " "
    d = d + _[1]
    return d

def formare_link_partial_cautare_personalizata(keywords):
    """
    Functia primeste ca si parametru un string, reprezentand un set de unul sau mai multe cuvinte ce vor fi utilizate
    in cautarea personalizata. Functia returneaza un string reprezentand o parte din link-ul utilizat in aceeasi cautare.
    ex: "huawei p9" => "huawei%20p9"
    :param keywords:
    :return:
    """
    _ = keywords.split()
    keywords = ""
    for i in range(0, len(_) - 1):
        keywords = keywords + _[i] + "%20"
    keywords = keywords + _[len(_) - 1]
    return keywords

def reparator_nume_imagini(nume):
    """
    Functia primeste ca si parametru un string, reprezentand numele imaginilor unui produs, si verifica daca exista
    caracterul " ' " in el si il elimina, in caz afirmativ pentru ca provoaca o eroare la codul HTML.
    ex: "Casti Skullcandy Ink'd" => "Casti Skullcandy Inkd"
    :param title:
    :return:
    """
    if "'" in nume:
        nume = nume.split("'")
        _ = ""
        for i in range(0, len(nume)):
            _ = _ + nume[i]
        nume = _
    return nume