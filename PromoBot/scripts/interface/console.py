autor = "Ursu Alin"
import os
import sys
from sys import exit
import time
import colorama

from scripts import utils
from scripts.EMAG import emag_main_search
from scripts.ALTEX import altex_main_search
from scripts.CEL import cel_main_search
from scripts.SPORTVISION import sportvision_main_search
from scripts.PRONUTRITION import pronutrition_main_search
from scripts.scrappers.emag import Emag
from scripts.scrappers.altex import Altex
from scripts.scrappers.constantinnautics import ConstantinNautics
from scripts.scrappers.cel import Cel
from scripts.scrappers.sportvision import Sportvision
from scripts.scrappers.lavas import Lavas
from scripts.scrappers.pronutrition import ProNutrition
from scripts.debug import Logger

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
binpath = path + "bin" + slash
datapath = binpath + "data" + slash
imagespath = datapath + "images" + slash
htmlpath = binpath + "html" + slash
jsonpath = binpath + "json" + slash
colorama.init()

def Clear():
    """
    Functie ce goleste ecranul programului de orice informatie.
    :return:
    """
    print(100 * "\n")
def Quit():
    """
    Functie folosita pentru a inchide programul.
    :return:
    """
    q = input("Apasa ENTER pentru a inchide programul.")
    exit()

def Console():
    """
    Programul principal in formatul consolei.
    :return:
    """
    log = Logger()
    Clear()
    print(autor)
    time.sleep(2)

    print("\n")
    if utils.verif_fisiere_html_prezente() == 1:
        print(colorama.Fore.YELLOW + "Au fost detectate fisiere din cautarile anterioare. Doriti stergerea acestora?" + colorama.Fore.WHITE)
        action = ""
        while action == "":
            action = input(" 1 - DA ; 0 - NU : ")
            try:
                action = int(action)
            except:
                print(colorama.Fore.RED + "Valoare invalida!" + colorama.Fore.WHITE)
                action = ""
            if action != "" and action != 1 and action != 0:
                print(colorama.Fore.RED + "Valoare invalida!" + colorama.Fore.WHITE)
                action = ""

        if action == 1:
            log.scriere("Sterg fisierele din cautarile anterioare.")
            utils.stergere_html()
            print(colorama.Fore.GREEN + "Stergere finalizata!"+ colorama.Fore.WHITE)
            time.sleep(2)
        print("\n")

    site = utils.alegere_site()
    print("\n")
    if site == 1:
        log.scriere("Incep preluarea datelor de pe Emag.")
        cautare = emag_main_search.tip_cautare()
        if cautare == 1:
            categorie = emag_main_search.selectare_categorie()
            print("\n")
            suma_maxima = emag_main_search.suma_maxima()
        else:
            categorie = emag_main_search.keywords_cautare()
            print("\n")
        pagini = emag_main_search.numar_pagini()

        inainte = utils.numar_fisiere_html_prezente()
        print("Incep cautarea... (" + colorama.Fore.YELLOW + "poate dura pana la cateva minute!" + colorama.Fore.WHITE + ")")
        if cautare == 1:
            Emag(categorie, suma_maxima, pagini)
        else:
            Emag(categorie, None, pagini, cautare="personalizata")
        dupa = utils.numar_fisiere_html_prezente()
        print(colorama.Fore.GREEN + "Cautare finalizata!" + colorama.Fore.WHITE)
        log.scriere("Au fost gasite {} reduceri.".format(dupa-inainte))
        print("Am gasit {} reduceri ce corespund parametrilor dumneavoastra!".format(dupa-inainte))

    elif site == 2:
        log.scriere("Incep preluarea datelor de pe Altex.")
        categorie = altex_main_search.selectare_categorie()
        print("\n")
        suma_maxima = altex_main_search.suma_maxima()
        pagini = altex_main_search.numar_pagini()

        inainte = utils.numar_fisiere_html_prezente()
        print("Incep cautarea... (" + colorama.Fore.YELLOW + "poate dura pana la cateva minute!" + colorama.Fore.WHITE + ")")
        Altex(categorie, suma_maxima, pagini)
        dupa = utils.numar_fisiere_html_prezente()
        print(colorama.Fore.GREEN + "Cautare finalizata!" + colorama.Fore.WHITE)
        log.scriere("Au fost gasite {} reduceri.".format(dupa - inainte))
        print("Am gasit {} reduceri ce corespund parametrilor dumneavoastra!".format(dupa-inainte))

    elif site == 3:
        log.scriere("Incep preluarea datelor de pe ConstantinNautics.")
        print("\n")

        inainte = utils.numar_fisiere_html_prezente()
        print("Incep cautarea... (" + colorama.Fore.YELLOW + "poate dura pana la cateva minute!" + colorama.Fore.WHITE + ")")
        ConstantinNautics()
        dupa = utils.numar_fisiere_html_prezente()
        print(colorama.Fore.GREEN + "Cautare finalizata!" + colorama.Fore.WHITE)
        log.scriere("Au fost gasite {} reduceri.".format(dupa - inainte))
        print("Am gasit {} reduceri ce corespund parametrilor dumneavoastra!".format(dupa - inainte))

    elif site == 4:
        log.scriere("Incep preluarea datelor de pe Cel.")
        cautare = cel_main_search.tip_cautare()
        if cautare == 1:
            categorie = cel_main_search.selectare_categorie()
        else:
            categorie = cel_main_search.keywords_cautare()
        print("\n")
        pagini = cel_main_search.numar_pagini()

        inainte = utils.numar_fisiere_html_prezente()
        print("Incep cautarea... (" + colorama.Fore.YELLOW + "poate dura pana la cateva minute!" + colorama.Fore.WHITE + ")")
        if cautare == 1:
            Cel(categorie, pagini)
        else:
            Cel(categorie, pagini, cautare="personalizata")
        dupa = utils.numar_fisiere_html_prezente()
        print(colorama.Fore.GREEN + "Cautare finalizata!" + colorama.Fore.WHITE)
        log.scriere("Au fost gasite {} reduceri.".format(dupa - inainte))
        print("Am gasit {} reduceri ce corespund parametrilor dumneavoastra!".format(dupa - inainte))

    elif site == 5:
        log.scriere("Incep preluarea datelor de pe Sportvision.")
        cautare = sportvision_main_search.tip_cautare()
        if cautare == 1:
            categorie = sportvision_main_search.selectare_categorie()
        else:
            categorie = sportvision_main_search.keywords_cautare()
        print("\n")
        pagini = sportvision_main_search.numar_pagini()

        inainte = utils.numar_fisiere_html_prezente()
        print("Incep cautarea... (" + colorama.Fore.YELLOW + "poate dura pana la cateva minute!" + colorama.Fore.WHITE + ")")
        if cautare == 1:
            Sportvision(categorie, pagini)
        else:
            Sportvision(categorie, pagini, cautare="personalizata")
        dupa = utils.numar_fisiere_html_prezente()
        print(colorama.Fore.GREEN + "Cautare finalizata!" + colorama.Fore.WHITE)
        log.scriere("Au fost gasite {} reduceri.".format(dupa - inainte))
        print("Am gasit {} reduceri ce corespund parametrilor dumneavoastra!".format(dupa - inainte))

    elif site == 6:
        log.scriere("Incep preluarea datelor de pe Lavas.")
        print("\n")

        inainte = utils.numar_fisiere_html_prezente()
        print("Incep cautarea... (" + colorama.Fore.YELLOW + "poate dura pana la cateva minute!" + colorama.Fore.WHITE + ")")
        Lavas()
        dupa = utils.numar_fisiere_html_prezente()
        print(colorama.Fore.GREEN + "Cautare finalizata!" + colorama.Fore.WHITE)
        log.scriere("Au fost gasite {} reduceri.".format(dupa - inainte))
        print("Am gasit {} reduceri ce corespund parametrilor dumneavoastra!".format(dupa - inainte))

    elif site == 7:
        log.scriere("Incep preluarea datelor de pe Pro Nutrition.")
        print("\n")
        pagini = pronutrition_main_search.numar_pagini()

        inainte = utils.numar_fisiere_html_prezente()
        print("Incep cautarea... (" + colorama.Fore.YELLOW + "poate dura pana la cateva minute!" + colorama.Fore.WHITE + ")")
        ProNutrition(pagini)
        dupa = utils.numar_fisiere_html_prezente()
        print(colorama.Fore.GREEN + "Cautare finalizata!" + colorama.Fore.WHITE)
        log.scriere("Au fost gasite {} reduceri.".format(dupa - inainte))
        print("Am gasit {} reduceri ce corespund parametrilor dumneavoastra!".format(dupa - inainte))
    if dupa-inainte != 0:
        from scripts.interface.gui import viewer_app
        viewer_app()
    print("\n")
    Quit()