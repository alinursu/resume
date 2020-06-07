autor = "Ursu Alin"
import sys
from sys import exit
import os
import colorama

from scripts import utils
from scripts.interface.console import Console
from scripts.interface.gui import GUI

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd()
cfgfile = "config.cfg"
colorama.init()

def Quit():
    """
    Functie ce inchide programul.
    :return:
    """
    q = input("Apasa ENTER pentru a inchide programul.")
    exit()

def main():
    """
    Programul principal.
    :return:
    """
    # Citesc setarile din "config.cfg"
    setari = {}
    with open(cfgfile, "r") as f:
        s = f.read().split("\n")

    # Scap de string-urile goale
    ok = 0
    while ok == 0:
        ok = 1
        try:
            for i in range(0, len(s)):
                if utils.verificare_string_gol(s[i]) == True:
                    del s[i]
                    ok = 0
        except:
            pass

    # Scap de comentarii
    ok = 0
    while ok == 0:
        ok = 1
        try:
            for i in range(0, len(s)):
                if "#" in s[i]:
                    del s[i]
                    ok = 0
        except:
            pass

    # Salvez setarile intr-o variabila de tip dictionary
    for sett in s:
        sett = sett.split("=")
        setari[sett[0]] = eval(sett[1])

    if setari["INTERFACE"] == "console":
        Console()
    elif setari["INTERFACE"] == "gui":
        GUI(setari["AUTHOR_WINDOW"])
    else:
        print(colorama.Fore.RED + "Eroare config.cfg: Interfata invalida!" + colorama.Fore.WHITE)
        Quit()



if __name__ == '__main__':
    main()
