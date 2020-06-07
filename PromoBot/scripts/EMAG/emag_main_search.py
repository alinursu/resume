autor = "Ursu Alin"
import os
import sys
import colorama

from scripts.EMAG import emag_string

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
    categorii = {1:"Laptopuri", 2:"Genti Laptop", 3:"Desktop PC", 4:"Placi Video", 5:"Procesoare", 6:"Placi de baza",
                 7:"Solid-State Drive",8:"Hard Disk-uri", 9:"Memorii", 10:"Carcase PC", 11: "Surse PC", 12:"Mouse",
                 13:"Tastaturi", 14:"Boxe PC", 15:"Casti PC",  16:"Memorii USB", 17:"Tablete Grafice",
                 18:"Console Gaming", 19:"Jocuri PC", 20:"Telefoane Mobile", 21:"Tablete",
                 22:"Imprimante Laser", 23:"Imprimante Inkjet", 24:"Smartwatch", 25:"Bratari Fitness", 26:"Boxe HI-FI",
                 27:"Boxe Portabile", 28:"Casti Audio", 29:"Aparate Foto DSLR", 30:"Televizoare", 31:"Frigidere", 32:"Aragazuri",
                 33:"Cuptoare cu Microunde", 34:"Espressor", 35:"Aspiratoare", 36:"Aparate Aer-Conditionat",
                 37:"Centrale Termice", 38:"Masini de Spalat Rufe", 39:"Masini de Spalat Vase"}

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
    keywords = emag_string.formare_link_partial_cautare_personalizata(keywords)
    return keywords