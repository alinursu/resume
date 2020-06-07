autor = "Ursu Alin"
from scripts import utils

def formare_descriere(desc):
    """
    Functie ce preia un string, reprezentand descrierea unui produs, si returneaza o lista, fiecare element reprezentand
    o propozitie din descriere.
    eliminand caractere inutile (ex: "\xa0").
    :param desc:
    :return:
    """
    desc = desc.split("\xa0")
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
        _ = []
        for char in desc[i]:
            _.append(char)
        while _[0] == " ":
            del _[0]
        while _[-1] == " ":
            del _[-1]

        desc[i] = " "
        for char in _:
            desc[i] = desc[i] + char

    return desc

def formare_specificatii(specs):
    """
    Functie ce formateaza scrisul din 'specs' (scapa de "\n" de la inceput si sfarsit).
    :param specs:
    :return:
    """
    s = {}

    for key in specs.keys():
        _ = {}
        for k in specs[key].keys():
            __ = k.split("\n")
            try:
                while utils.verificare_string_gol(__[0]) == True:
                    del __[0]
            except:
                pass
            try:
                while utils.verificare_string_gol(__[-1]) == True:
                    del __[-1]
            except:
                pass
            __ = __[0]
            ___ = specs[key][k].split("\n")
            try:
                while utils.verificare_string_gol(___[0]) == True:
                    del ___[0]
            except:
                pass
            try:
                while utils.verificare_string_gol(___[-1]) == True:
                    del ___[-1]
            except:
                pass
            try:
                ___ = ___[0]
            except:
                pass
            _[__] = ___
        __ = key.split("\n")
        try:
            while utils.verificare_string_gol(__[0]) == True:
                del __[0]
        except:
            pass
        try:
            while utils.verificare_string_gol(__[-1]) == True:
                del __[-1]
        except:
            pass
        __ = __[0]
        s[__] = _

    return s

def transformare_pret_int(pret):
    """
    Functie ce transforma pretul din string in intreg. Folosita pentru a adauga date in baza de date.
    (ex: "3999 Lei" => 4000)
    :param pret:
    :return:
    """
    return int(pret.split(" ")[0]) + 1

def link_cadou_imagine(link):
    """
    Functia primeste ca si parametru un string, reprezentand link-ul catre o imagine a unui cadou, si returneaza
    link-ul prelucrat.
    ex: "http://s.cel.ro//includes/templates/cel/images/no_picture.gif" => "http://s.cel.ro/includes/templates/cel/images/no_picture.gif"
    :param link:
    :return:
    """
    _ = link.split("//")
    link = ""
    if len(_) == 2:
        link = "{}//{}".format(_[0], _[1])
    else:
        link = _[0] + "//"
        for i in range(1, len(_)-1):
            link = link + _[i] + "/"
        link = link + _[-1]
    return link

def formare_link_partial_cautare_personalizata(keywords):
    """
    Functia primeste ca si parametru un string, reprezentand un set de unul sau mai multe cuvinte ce vor fi utilizate
    in cautarea personalizata. Functia returneaza un string reprezentand o parte din link-ul utilizat in aceeasi cautare.
    ex: "huawei p9" => "huawei+p9"
    :param keywords:
    :return:
    """
    _ = keywords.split()
    keywords = ""
    for i in range(0, len(_) - 1):
        keywords = keywords + _[i] + "+"
    keywords = keywords + _[len(_) - 1]
    return keywords