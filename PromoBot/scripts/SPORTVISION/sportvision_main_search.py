autor = "Ursu Alin"
import os
import sys
import colorama

from scripts.SPORTVISION import sportivision_string

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
    categorii = {1:"Incaltaminte Sport Barbati", 2:"Incaltaminte Sport Femei", 3:"Incaltaminte Sport Copii",
                 4:"Produse Adidas", 5:"Produse Champion", 6:"Produse Converse", 7:"Produse Lonsdale",
                 8:"Produse New Balance", 9:"Produse Nike", 10:"Produse Puma", 11:"Produse Reebok",
                 12:"Produse Under Armour", 13:"Produse Timberland"}

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
    keywords = sportivision_string.formare_link_partial_cautare_personalizata(keywords)
    return keywords