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