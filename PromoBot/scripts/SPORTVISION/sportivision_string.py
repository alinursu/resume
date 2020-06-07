autor = "Ursu Alin"
from scripts import utils

def formare_pret(pret):
    """
    Functia primeste ca si parametru un string, reprezentand un pret si scapa de caractere neimportante.
    ex: "\n524,00\nRON\n" => "524,00 RON"
    :param pret:
    :return:
    """
    pret = pret.split("\n")

    ok = 0
    while ok == 0:
        ok = 1
        for i in range(0, len(pret)):
            try:
                if utils.verificare_string_gol(pret[i]) == True:
                    del pret[i]
                    ok = 0
            except:
                break
    _ = ""
    for i in range(0, len(pret)-1):
        _ = _ + pret[i] + " "
    _ = _ + pret[len(pret)-1]
    pret = _
    return pret

def formare_descriere(desc):
    """
    Functia primeste ca si parametru un string, reprezentand descrierea unui produs, si scapa de caractere si spatii inutile.
    ex: '\r\n                         Pantofi sport Alergare Adulti NIKE                    '
    => 'Pantofi sport Alergare Adulti NIKE'
    :param desc:
    :return:
    """
    _ = desc
    desc = desc.split("\r")[-1]
    desc = desc.split("\n")[-1]

    desc = desc.split(" ")

    ok = 0
    while ok == 0:
        ok = 1
        try:
            for i in range(0, len(desc)):
                if desc[i] == '':
                    del desc[i]
                    ok = 0
        except:
            pass

    try:
        aux = ""
        for i in range(0, len(desc)-1):
            aux = aux + desc[i] + ' '
        aux = aux + desc[len(desc)-1]
        desc = aux
        aux = []
        aux.append(desc)
        desc = aux
    except:
        __ = _.split("\r")[-1].split("\n")
        desc = []
        for string in __:
            if len(string) != 0:
                desc.append(string)
                break

    return desc

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