autor = "Ursu Alin"
from scripts import utils

def formare_pret_vechi(pret):
    """
    Functie ce preia un pret si il reformeaza.
    Ex: "3.499,90" => "3.499,90 Lei"
    :return:
    """
    pret = pret + " Lei"
    return pret

def formare_pret_nou(pret):
    """
    Functie ce preia un pret si il reformeaza.
    Ex: "2.503,90lei" => "2.503,90 Lei"
    :param pret:
    :return:
    """
    pret = pret.split("lei")[0] + " Lei"
    return pret

def formare_pret_reducere(pret):
    """
    Functie ce preia un pret si il reformeaza.
    Ex: "Reducere900\xa0lei" => "900 Lei"
    :param pret:
    :return:
    """
    pret = pret.split("\xa0")[0].split("Reducere")[1].split(" ")[0]
    if "%" not in pret:
        pret = pret + " Lei"
    else:
        pret = pret.split(" ")[0] + "%"
    return pret

def eliminare_spatii(string):
    """
    Functie ce primeste un string si sterge spatiile libere din inaintea scrisului si de dupa scris.
    Ex: "   exemplu  " => "exemplu"
    :param string:
    :return:
    """
    _ = []
    for char in string:
        _.append(char)

    while _[0] == ' ':
        del _[0]
    while _[len(_)-1] == ' ':
        del _[len(_)-1]

    string = ""
    for char in _:
        string = string + char

    return string

def formare_descriere(text):
    """
    Functie ce primeste ca si parametru un text reprezentand descrierea unui produs si inlatura anumite caractere
    (ex: "\n") si transforma string-ul intr-o lista, fiecare element reprezentand o propozitie a descrierii
    :param text:
    :return:
    """
    text = text.split("\n")
    ok = 0
    while ok == 0:
        ok = 1
        for i in range(0, len(text)):
            try:
                if utils.verificare_string_gol(text[i]) == 1:
                    ok = 0
                    del text[i]
            except:
                break

    t = []
    for i in range(0,len(text)):
        if "." not in text[i]:
            t.append(text[i])
        else:
            _ = text[i].split(".")
            for j in range(0, len(_)-1):
                t.append(_[j] + ".")

    for i in range(0 ,len(t)):
        t[i] = eliminare_spatii(t[i])

    return t

def verificare_functie_initFlix(text):
    """
    Functie ce verifica daca in lista de string-uri, reprezentand descrierea, exista functia 'initFlix', functie ce
    apare din cauza lipsei descrierii de pe site-ul Altex.
    :param text:
    :return:
    """
    ok = 0
    for i in range(0, len(text)):
        if "initFlix" in text[i]:
            ok = 1
            break
    return ok

def stergere_functie_initFlix(text):
    """
    Functie ce sterge din lista de string-uri, reprezentand descrierea, functia 'initFlix', functie ce apare din cauza
    lipsei descrierii de pe site-ul Altex.
    :param text:
    :return:
    """
    n = 0
    for i in range(0, len(text)):
        if "initFlix" in text[i]:
            n = i
            break

    try:
        while(len(text[n]) != 0):
            del text[n]
    except:
        pass

    return text

def formare_matrice(text):
    """
    Functie ce preia un string ca si parametru, reprezentand un link, si returneaza o "matrice" cu ajutorul careia se
    vor forma link-urile pentru descarcarea imaginilor.
    ex: "https://cdna.altex.ro/resize/media/catalog/product/S/M/2bd48d28d1c32adea0e55139a4e6434a/SMTG960FZKD-1_964bbb6e.jpg"
    => "https://cdna.altex.ro/resize/media/catalog/product/S/M/2bd48d28d1c32adea0e55139a4e6434a/{}"
    :param text:
    :return:
    """
    text = text.split("/")
    _ = ""
    for i in range(0, len(text)-1):
        _ = _ + text[i] + "/"
    _ = _ + "{}"
    text = _
    return text
