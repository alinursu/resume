autor = "Ursu Alin"
import os
import sys
import colorama

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
imagespath = path + "bin" + slash + "data" + slash + "images" + slash
htmlpath = path + "bin" + slash + "html" + slash
colorama.init()

def selectare_categorie():
    """
    Functie ce solicita utilizatorului sa aleaga o anumita categorie in care vor fi cautate produse.
    :return:
    """
    categorii = {1:"Telefoane", 2:"Smartwatch", 3:"Boxe portabile", 4:"Casti", 5:"Tablete", 6:"Laptopuri",
                 7:"Sisteme PC", 8:"Hard Disk-uri", 9:"Solid State Drive-uri", 10:"Placi Video", 11:"Placi de Baza",
                 12:"Procesoare", 13:"Memorii RAM", 14:"Surse de Alimentare", 15:"Carcase", 16:"HDD Extern",
                 17:"Memorii USB", 18:"Boxe Calculator", 19:"Imprimante", 20:"Console PlayStation 4",
                 21:"Console Xbox One", 22:"Jocuri PC", 23:"Televizoare", 24:"Sisteme Audio", 25:"Soundbar si Home Cinema",
                 26:"Videoproiectoare", 27:"Aer Conditionat", 28:"Masini de Spalat Rufe", 29:"Frigidere",
                 30:"Masini de Spalat Vase", 31:"Expresoare Cafea"}

    for key in categorii.keys():
        print("     - {} - {}".format(key, categorii[key]))
    categorie = ""
    while categorie == "":
        categorie = input(" >> ")
        try:
            categorie = int(categorie)
        except:
            categorie = ""
            print(colorama.Fore.RED + "Valoare invalida!" + colorama.Fore.WHITE)

        if categorie != "" and categorie not in categorii.keys():
            categorie = ""
            print(colorama.Fore.RED + "Valoare invalida!" + colorama.Fore.WHITE)

    return categorii[categorie]


def suma_maxima():
    """
    Functie ce solicita utilizatorului sa introduca o suma maxima in care se vor incadra produsele.
    :return:
    """
    sum = ""
    while sum == "":
        sum = input("Suma maxima in care se vor incadra produsele (ENTER pentru nicio limita): ")
        if sum != "":
            try:
                sum = int(sum)
            except:
                sum = ""
                print(colorama.Fore.RED + "Valoare invalida!" + colorama.Fore.WHITE)
        else:
            sum = None

    return sum

def numar_pagini():
    """
    Functie ce solicita utilizatorului sa introduca numarul de pagini in care se vor cauta produse la promotie.
    :return:
    """
    numar = ""
    while numar == "":
        numar = input("Numarul de pagini (ENTER pentru toate): ")
        if numar != "":
            try:
                numar = int(numar)
                if numar > 10:
                    print(colorama.Fore.YELLOW + "Cautarea nu trebuie sa depaseaza 10 pagini!" + colorama.Fore.WHITE)
                    numar = ""
                elif numar == 0:
                    print(colorama.Fore.YELLOW + "Numarul introdus trebuie sa fie nenul!" + colorama.Fore.WHITE)
                    numar = ""
                elif numar < 0:
                    print(colorama.Fore.YELLOW + "Numarul introdus trebuie sa fie natural!" + colorama.Fore.WHITE)
                    numar = ""
            except:
                numar = ""
                print(colorama.Fore.RED + "Valoare invalida!" + colorama.Fore.WHITE)
        else:
            numar = None

    return numar

def tip_cautare():
    """
    Functie ce solicita utilizatorului sa aleaga tipul de cautare: dupa categorie sau personalizata.
    :return:
    """
    print("Va rog sa alegeti tipul de cautare: ")
    print("     1 - Dupa categorie")
    print("     2 - Personalizata")
    cautare = ""
    while cautare == "":
        cautare = input(" >> ")
        try:
            cautare = int(cautare)
        except:
            cautare = ""
            print(colorama.Fore.RED + "Valoare invalida!" + colorama.Fore.WHITE)
        if cautare != 1 and cautare != 2:
            cautare = ""
            print(colorama.Fore.RED + "Valoare invalida!" + colorama.Fore.WHITE)
    return cautare

def keywords_cautare():
    """
    Functie ce solicita utilizatorului sa introduca un set de cuvinte ce vor fi folosite pentru cautarea personalizata.
    :return:
    """
    keywords = ""
    while len(keywords) == 0:
        keywords = input("Va rog introduceti ce doriti sa cautati: ")
        if len(keywords) == 0:
            print(colorama.Fore.RED + "Valoare invalida!" + colorama.Fore.WHITE)
    _ = keywords.split()
    keywords = ""
    for i in range(0,len(_)-1):
        keywords = keywords + _[i] + "%20"
    keywords = keywords + _[len(_)-1]
    return keywords