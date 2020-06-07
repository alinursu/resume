autor = "Ursu Alin"
import os
import sys
import datetime

from scripts import utils

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
datapath = path + "bin" + slash + "data" + slash
imagespath = datapath + "imagini" + slash
htmlpath = path + "bin" + slash + "html" + slash
rawpath = datapath + "raw" + slash
punctuatie = [".", "!", "?"]
rawfn = "electronice.code"
rawfn_gift = "electronice_gift.code"
rawfn_nautics = "nautics.code"
rawfn_sportvision = "sportvision.code"
rawfn_pronutrition = "pronutrition.code"

def formare_data():
    """
    Functie ce formeaza un string ce contine informatii despre data zilei actuale (format: "ZI-LUNA-AN").
    :return:
    """
    now = datetime.datetime.now()
    if now.day < 10:
        d = "0{}".format(str(now.day))
    else:
        d = str(now.day)
    if now.month < 10:
        m = "0{}".format(str(now.month))
    else:
        m = str(now.month)
    y = str(now.year)

    data = "{}.{}.{}".format(d,m,y)
    return data

def creatorHTML_pronutrition(info):
    """
    Functie ce creeaza un fisier HTML pe baza informatiilor primite ca si parametru, prelucrand codul brut din
    PRONUTRITION.CODE.
    :param info:
    :return:
    """
    # Citesc codul HTML brut
    os.chdir(rawpath)
    with open(rawfn_pronutrition, "r") as f:
        raw = f.read()
    raw = raw.split("##########SPLIT##########")
    os.chdir(path)

    # Formez codul HTML din codul brut
    html = ""
    dim = utils.redimensionare_imagine(info["imagini"][0], True)
    html = html + raw[0].format(info["titlu"], info["titlu"], info["imagini"][0], dim[0], dim[1], info["pret"]["vechi"], info["pret"]["nou"], info["pret"]["discount"], info["rating"]["rata"], info["rating"]["review-uri"])
    for d in info["descriere"]:
        html = html + raw[1].format(d) + "\n"
    html = html + raw[2]
    for key in info["specs"].keys():
        html = html + raw[3].format(key)
        for spec in info["specs"][key]:
            html = html + raw[4].format(spec, info["specs"][key][spec])
        html = html + raw[5]
    html = html + raw[6].format(formare_data(), info["link"])

    # Salvez fisierul HTML
    t = info["titlu"].split(" ")
    fn = ""
    try:
        for i in range(0, 10):
            fn = fn + t[i] + " "
    except:
        pass
    fn = fn + ".html"
    os.chdir(htmlpath)
    with open(fn, "w") as f:
        f.write(html)
    os.chdir(path)


def creatorHTML_sportvision(info):
    """
    Functie ce creeaza un fisier HTML pe baza informatiilor primite ca si parametru, prelucrand codul brut din
    SPORTVISION.CODE.
    :param info:
    :return:
    """
    # Citesc codul HTML brut
    os.chdir(rawpath)
    with open(rawfn_sportvision, "r") as f:
        raw = f.read()
    raw = raw.split("##########SPLIT##########")
    os.chdir(path)

    # Formez codul HTML din codul brut
    html = ""
    dim = utils.redimensionare_imagine(info["imagini"][0], True)
    html = html + raw[0].format(info["titlu"], info["titlu"], info["imagini"][0], dim[0], dim[1], info["pret"]["vechi"], info["pret"]["nou"], info["pret"]["discount"])
    _ = raw[1].split("\n")
    for d in info["descriere"]:
        ok = 0
        for p in punctuatie:
            if p in d:
                ok = 1
                break
        if ok == 0:
            html = html + _[1].format(d) + "\n"
        else:
            html = html + _[2].format(d) + "\n"
    html = html + raw[2]
    for img in info["imagini"]:
        dim = utils.redimensionare_imagine(img)
        html = html + raw[3].format(img, dim[0], dim[1])
    html = html + raw[4]
    html = html + raw[5].format("Specificatii")
    for key in info["specs"].keys():
        html = html + raw[6].format(key, info["specs"][key])
    html = html + raw[7]
    html = html + raw[8].format(formare_data(), info["link"])

    # Salvez fisierul HTML
    t = info["titlu"].split(" ")
    fn = ""
    try:
        for i in range(0, 10):
            fn = fn + t[i] + " "
    except:
        pass
    fn = fn + ".html"
    os.chdir(htmlpath)
    with open(fn, "w") as f:
        f.write(html)
    os.chdir(path)


def creatorHTML_nautics(info):
    """
    Functie ce creeaza un fisier HTML pe baza informatiilor primite ca si parametru, prelucrand codul brut din
    NAUTICS.CODE.
    :param info:
    :return:
    """
    # Citesc codul HTML brut
    os.chdir(rawpath)
    with open(rawfn_nautics, "r") as f:
        raw = f.read()
    raw = raw.split("##########SPLIT##########")
    os.chdir(path)

    # Formez codul HTML din codul brut
    html = ""
    dim = utils.redimensionare_imagine(info["imagini"][0], True)
    html = html + raw[0].format(info["titlu"], info["titlu"], info["imagini"][0], dim[0], dim[1], info["pret"]["vechi"], info["pret"]["nou"], info["pret"]["discount"])
    _ = raw[1].split("\n")
    for d in info["descriere"]:
        __ = 1
        for p in punctuatie:
            if p in d:
                __ = 0
                break
        if __ == 0:
            html = html + _[2].format(d) + "\n"
        elif __ == 1:
            html = html + _[1].format(d) + "\n"
    html = html + raw[2]
    for img in info["imagini"]:
        dim = utils.redimensionare_imagine(img)
        html = html + raw[3].format(img, dim[0], dim[1])
    html = html + raw[4].format(formare_data(), info["link"])

    # Salvez fisierul HTML
    t = info["titlu"].split(" ")
    fn = ""
    try:
        for i in range(0, 10):
            fn = fn + t[i] + " "
    except:
        pass
    fn = fn + ".html"
    os.chdir(htmlpath)
    with open(fn, "w") as f:
        f.write(html)
    os.chdir(path)

def creatorHTML_gift(info):
    """
    Functie ce creeaza un fisier HTML pe baza informatiilor primite ca si parametru, prelucrand codul brut din
    ELECTRONICE_GIFT.CODE
    :param info:
    :return:
    """
    # Citesc codul HTML brut
    os.chdir(rawpath)
    with open(rawfn_gift, "r") as f:
        raw = f.read()
    raw = raw.split("##########SPLIT##########")
    os.chdir(path)

    # Formez codul HTML din codul brut
    html = ""
    dim = utils.redimensionare_imagine(info["imagini"][0], True)
    dim_img = utils.redimensionare_imagine(info["cadou"]["imagine"], None)
    html = html + raw[0].format(info["titlu"], info["titlu"], info["imagini"][0], dim[0], dim[1], info["pret"]["vechi"], info["pret"]["nou"], info["pret"]["discount"], info["rating"]["rata"], info["rating"]["review-uri"], info["cadou"]["imagine"], dim_img[0], dim_img[1], info["cadou"]["titlu"], info["cadou"]["pret"], info["cadou"]["link"])
    t = raw[1].split("\n")
    for d in info["descriere"]:
        _ = 1
        for p in punctuatie:
            if p in d:
                _ = 0
                break
        if d.split(" ")[0] == "-":
            html = html + t[2].format(d) + "\n"
        # if "." not in d:
        elif _ == 1:
            html = html + t[1].format(d) + "\n"
        else:
            html = html + t[2].format(d) + "\n"
    html = html + raw[2]
    for i in range(1, len(info["imagini"])):
        dim = utils.redimensionare_imagine(info["imagini"][i])
        html = html + raw[3].format(info["imagini"][i], dim[0], dim[1])
    html = html + raw[4]
    for key in info["specs"].keys():
        html = html + raw[5].format(key)
        for spec in info["specs"][key]:
            html = html + raw[6].format(spec, info["specs"][key][spec])
        html = html + raw[7]
    html = html + raw[8].format(formare_data(), info["link"])

    # Salvez fisierul HTML
    t = info["titlu"].split(" ")
    fn = ""
    try:
        for i in range(0, 10):
            fn = fn + t[i] + " "
    except:
        pass
    fn = fn + ".html"
    os.chdir(htmlpath)
    with open(fn, "w") as f:
        f.write(html)
    os.chdir(path)


def creatorHTML(info):
    """
    Functie ce creeaza un fisier HTML pe baza informatiilor primite ca si parametru, prelucrand codul brut din
    ELECTRONICE.CODE.
    :param info:
    :return:
    """
    # Citesc codul HTML brut
    os.chdir(rawpath)
    with open(rawfn, "r") as f:
        raw = f.read()
    raw = raw.split("##########SPLIT##########")
    os.chdir(path)

    # Formez codul HTML din codul brut
    html = ""
    dim = utils.redimensionare_imagine(info["imagini"][0], True)
    html = html + raw[0].format(info["titlu"], info["titlu"], info["imagini"][0], dim[0], dim[1], info["pret"]["vechi"], info["pret"]["nou"], info["pret"]["discount"], info["rating"]["rata"], info["rating"]["review-uri"])
    t = raw[1].split("\n")
    for d in info["descriere"]:
        _ = 1
        for p in punctuatie:
            if p in d:
                _ = 0
                break
        if d.split(" ")[0] == "-":
            html = html + t[2].format(d) + "\n"
        # if "." not in d:
        elif _ == 1:
            html = html + t[1].format(d) + "\n"
        else:
            html = html + t[2].format(d) + "\n"
    html = html + raw[2]
    for i in range(1, len(info["imagini"])):
        dim = utils.redimensionare_imagine(info["imagini"][i])
        html = html + raw[3].format(info["imagini"][i], dim[0], dim[1])
    html = html + raw[4]
    for key in info["specs"].keys():
        html = html + raw[5].format(key)
        for spec in info["specs"][key]:
            html = html + raw[6].format(spec, info["specs"][key][spec])
        html = html + raw[7]
    html = html + raw[8].format(formare_data(), info["link"])

    # Salvez fisierul HTML
    t = info["titlu"].split(" ")
    fn = ""
    try:
        for i in range(0, 10):
            fn = fn + t[i] + " "
    except:
        pass
    fn = fn + ".html"
    os.chdir(htmlpath)
    with open(fn, "w") as f:
        f.write(html)
    os.chdir(path)


def transformare_string_pret(pret):
    """
    Functie ce transforma pretul integer in pret string.
    ex: 1500 => 1,500.00
    :param pret:
    :return:
    """
    pret_str = ""
    if pret < 1000:
        pret_str = str(pret) + ",00"
        return pret_str
    elif pret >= 1000:
        mii = int(pret/1000)
        sute = str(pret%1000)
        if len(sute) == 1:
            sute = "000"
        pret_str = str(mii) + "." + str(sute) + ",00"
        return pret_str

def HTML_adaugare_regasire(titlu_produs, data, pret):
    """
    Functie ce adauga un paragraf la titlu ce reprezinta faptul ca produsul a mai fost o data la reducere, la un pret mai mic.
    :param titlu_produs:
    :param data:
    :param pret:
    :return:
    """
    ph = '<p style="color: red;text-align:right;padding:0;border:0;margin:0;font-size:18px;">Pe data de {} a fost la pretul de {} lei!</p>'
    partial = ""
    _ = titlu_produs.split(" ")
    try:
        for i in range(0, 10):
            partial = partial + _[i] + " "
    except:
        pass

    html = ""
    for p in os.listdir(htmlpath):
        if partial in p:
            html = p
            break

    os.chdir(htmlpath)
    with open(html, "r") as f:
        code = f.read()
    code = code.split("\n")
    for i in range(0, len(code)):
        if 'class="title"' in code[i]:
            n = i
            break
    code.append(0)
    aux = ""
    aux2 = ""
    for i in range(0, len(code)):
        if i == n+1:
            aux = code[i]
            code[i] = ph.format(data, transformare_string_pret(pret))
        elif i > n+1:
            aux2 = code[i]
            code[i] = aux
            aux = aux2
        elif i == len(code)-1:
            code[i] = aux

    h = ""
    for i in range(0, len(code)):
        h = h + code[i] + "\n"

    with open(html, "w") as f:
        f.write(h)
    os.chdir(path)

