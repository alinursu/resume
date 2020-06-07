autor = "Ursu Alin"
import os
import sys
import colorama
import requests
import urllib3
import shutil
import datetime
from PIL import Image

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
imagespath = path + "bin" + slash + "data" + slash + "images" + slash
htmlpath = path + "bin" + slash + "html" + slash
colorama.init()

def verif_fisiere_html_prezente():
    """
    Functie ce verifica daca exista deja fisiere HTML formate in cautarile anterioare. Daca da, returneaza valoarea 1,
    daca nu, returneaza valoarea 0.
    :return:
    """
    fisiere = os.listdir(htmlpath)

    if len(fisiere) == 0:
        return 0
    else:
        return 1

def numar_fisiere_html_prezente():
    """
    Functie ce returneaza numarul actual de fisiere HTML formate in cautarile anterioare.
    :return:
    """
    return len(os.listdir(htmlpath))

def lista_fisiere_html():
    """
    Functie ce returneaza o lista ce contine numele fiecarui fisier HTML si calea catre fisier.
    :return:
    """
    return os.listdir(htmlpath)

def stergere_html():
    """
    Functie ce sterge toate fisierele HTML formate in cautarile anterioare si imaginile legate de acestea.
    :return:
    """
    os.chdir(htmlpath)
    fisiere = os.listdir(htmlpath)
    for fisier in fisiere:
        os.remove(fisier)

    os.chdir(imagespath)
    imagini = os.listdir(imagespath)
    for imagine in imagini:
        os.remove(imagine)

    os.chdir(path)

def alegere_site():
    """
    Functie ce solicita utilizatorului sa aleaga un anumit site dintr-o lista, site pe care se vor cauta mai apoi
    produse aflate la reducere.
    :return:
    """
    site_list = {1:"Emag", 2:"Altex", 3:"Constantin Nautics", 4:"Cel.ro", 5:"Sportvision", 6:"Lavas", 7:"Pro Nutrition"}
    site = ""
    print("Alegeti site-ul: ")
    for key in site_list.keys():
        print("     - {} - {}".format(key, site_list[key]))
    while site == "":
        site = input (" >> ")
        try:
            site = int(site)
        except:
            print(colorama.Fore.RED + "Valoare invalida!" + colorama.Fore.WHITE)
            site = ""

        if site != "" and site not in site_list.keys():
            print(colorama.Fore.RED + "Valoare invalida!" + colorama.Fore.WHITE)
            site = ""

    return site

def verificare_string_gol(string):
    """
    Functie ce verifica daca o valoare de tip STRING transmisa prin parametru este "goala" (contine numai spatii) sau nu.
    :param string:
    :return:
    """
    chars = ["a", "A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F", "g", "G", "h", "H", "i", "I", "j", "J",
             "k", "K", "l", "L", "m", "M", "n", "N", "o", "O", "p", "P", "q", "Q", "r" ,"R", "s", "S", "t", "T",
             "u", "U", "v", "V", "w", "W", "x", "X", "y", "Y", "z", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    ok = True
    for char in string:
        if char in chars:
            ok = False
            break
    return ok

def download_imagine(link, nume, extensie=None):
    """
    Functie ce descarca o anumita imagine de pe un link si o salveaza sub un anumit nume, transmise ca si parametru.
    :param link:
    :param nume:
    :return:
    """
    if extensie == None:
        extensie = link.split("/")[-1].split(".")[1]
    fn = "{}.{}".format(nume, extensie)

    os.chdir(imagespath)
    r = requests.get(link, stream=True)
    urllib3.disable_warnings()
    if r.status_code == 200:
        with open(fn, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    os.chdir(path)

def verificare_date(date, keywords):
    """
    Functie ce verifica daca un set de date de la un produs contine toate datele necesare pentru a se putea crea un fisier
    HTML.
    :param date:
    :param keywords:
    :return:
    """
    ok = True
    # Verific daca sunt toate elementele necesare comparand cheile necesare cu cheile din setul de informatii
    for key in keywords.keys():
        if key not in date.keys():
            ok = False
            break

    if ok == False:
        return ok
    else:
        # Verific daca toate elementele au toate subelementele necesare
        for key in keywords.keys():
            if type(keywords[key]) == list:
                for i in range(0, len(keywords[key])):
                    if keywords[key][i] not in date[key].keys():
                        ok = False
                        break
            if ok == False:
                break

    if ok == False:
        return ok
    else:
        # Verific daca toate elementele contin informatii sau nu
        for key in date.keys():
            if len(date[key]) == 0:
                ok = False
                break
        return ok

def stergere_set_imagini(nume_partial):
    """
    Functie ce sterge un set de imagini, imagini cautate cu ajutorul unui nume partial.
    :param nume_partial:
    :return:
    """
    os.chdir(imagespath)
    imgs = os.listdir(imagespath)
    for img in imgs:
        if nume_partial in img:
            os.remove(img)
    os.chdir(path)

def data_actuala():
    """
    Functia returneaza un string de format '{ZI}-{LUNA}-{AN}' reprezentand data actuala.
    :return:
    """
    now = datetime.datetime.now()
    if now.day >= 10:
        day = now.day
    else:
        day = '0' + str(now.day)
    if now.month >= 10:
        month = now.month
    else:
        month = '0' + str(now.month)
    data = "{}-{}-{}".format(day, month, now.year)
    return data

def redimensionare_imagine(img, imaginePrincipala=False):
    """
    Functie preia un string ca si parametru, reprezentand numele unei imagini, calculeaza lungimea si latimea imaginii
    si returneaza un set de valori intregi, reprezentand lungimea si latimea cu care vor aparea in fisierele HTML,
    pastrand totodata si aspectul (format: [lungime,latime]).
    In cazul in care parametrul 'imaginePrincipala' are valoarea True, inseamna ca este poza principala a unui produs,
    ea avand dimensiuni mai mari.
    In cazul in care parametrul 'imaginePrincipala' are valoarea None, inseamna ca este poza cadou, ea avand
    dimensiuni mai mici.
    :param img:
    :return:
    """
    # aspectRatio = lungimeVeche / latimeVeche
    # latimeNoua = lungimeNoua / aspectRatio
    # lungimeNoua = latimeNoua * aspectRatio
    os.chdir(imagespath)
    image = Image.open(img)
    os.chdir(path)
    lungime, latime = image.size
    if imaginePrincipala == True:
        # Patrat
        if lungime == latime:
            return [500, 500]
        # Widescreen
        elif lungime > latime:
            ratio = lungime / latime
            return [500, int(500/ratio)]
        # Portret
        elif lungime < latime:
            ratio = lungime / latime
            return [int(500*ratio), 500]
    elif imaginePrincipala == None:
        # Patrat
        if lungime == latime:
            return [200, 200]
        # Widescreen
        elif lungime > latime:
            ratio = lungime / latime
            return [200, int(200/ratio)]
        # Portret
        elif lungime < latime:
            ratio = lungime / latime
            return [int(200*ratio), 200]
    else:
        # Patrat
        if lungime == latime:
            return [250, 250]
        # Widescreen
        elif lungime > latime:
            ratio = lungime / latime
            return [250, int(250/ratio)]
        # Portret
        elif lungime < latime:
            ratio = lungime / latime
            return [int(250 * ratio), 250]

def redimensionare_imagine2(img, valoare):
    """
    Functie preia un string ca si parametru, reprezentand numele unei imagini, calculeaza lungimea si latimea imaginii
    si returneaza un set de valori intregi, reprezentand lungimea si latimea cu care vor aparea in fisierele HTML,
    pastrand totodata si aspectul (format: [lungime,latime]).
    :param img:
    :return:
    """
    # aspectRatio = lungimeVeche / latimeVeche
    # latimeNoua = lungimeNoua / aspectRatio
    # lungimeNoua = latimeNoua * aspectRatio
    os.chdir(imagespath)
    image = Image.open(img)
    os.chdir(path)
    lungime, latime = image.size
    if lungime > latime:
        ratio = lungime / latime
        return [valoare, int(valoare / ratio)]
    elif lungime < latime:
        ratio = lungime / latime
        return [valoare, int(valoare * ratio)]
    elif lungime == latime:
        return [valoare, valoare]

def verificare_prezenta_imagine(img):
    """
    Functia preia un string ca si parametru, reprezentand numele unei imagini, si verifica daca aceasta se afla in
    folderul 'images'. Returneaza valoarea True daca se afla si False in caz contrar.
    :param img:
    :return:
    """
    l = os.listdir(imagespath)
    for i in range(0, len(l)):
        if img in l[i]:
            return True
    return False