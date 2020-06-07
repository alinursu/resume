autor = "Ursu Alin"
import colorama

from scripts.CEL import cel_string

colorama.init()

def selectare_categorie():
    """
    Functie ce solicita utilizatorului sa aleaga o anumita categorie in care vor fi cautate produse.
    :return:
    """
    categorii = {1:"Laptopuri", 2:"Laptopuri Refubrished", 3:"Tablete", 4:"Telefoane", 5:"Smartwatch-uri",
                 6:"Boxe Portabile", 7:"Baterii Externe", 8:"Drone", 9:"Televizoare", 10:"Camere Video Sport",
                 11:"Sisteme Audio", 12:"Procesoare", 13:"Placi de Baza", 14:"Placi Video", 15:"Hard Disk-uri",
                 16:"Solid State Drive-uri", 17:"Casti", 18:"Boxe", 19:"Desktop-uri", 20:"Frigidere",
                 21:"Masini de Spalat Rufe", 22:"Aparate de Aer Conditionat", 23:"Centrale Termice"}

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
    keywords = cel_string.formare_link_partial_cautare_personalizata(keywords)
    return keywords