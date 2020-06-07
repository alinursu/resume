autor = "Ursu Alin"
import os
import sys
import colorama
import datetime

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
colorama.init()
cfgfn = "config.cfg"

class Logger:
    """
    Clasa folosita pentru a comunica cu fisierul 'log.txt' unde se salveaza un rezumat al utilizarii programului.
    Rezumatul contine data, ora si task-ul facut (ex: "Preiau informatii de pe www.test.ro").
    """
    def __init__(self):
        self.logfn = "log.txt"

    def data(self):
        """
        Functia creeaza un string ce contine data actuala (format: "ZI-LUNA-AN").
        :return:
        """
        now = datetime.datetime.now()
        if now.day > 10:
            day = now.day
        else:
            day = "0" + str(now.day)
        if now.month >= 10:
            month = now.month
        else:
            month = "0" + str(now.month)
        t = "{}-{}-{}".format(day, month, now.year)
        return t

    def ora(self):
        """
        Functia creeaa un string ce contine ora actuala. (format: "ORA:MINUT:SECUNDA")
        :return:
        """
        now = datetime.datetime.now()
        if now.second > 10:
            second = now.second
        else:
            second = "0" + str(now.second)
        if now.minute > 10:
            minute = now.minute
        else:
            minute = "0" + str(now.minute)
        if now.hour > 10:
            hour = now.hour
        else:
            hour = "0" + str(now.hour)
        t = "{}:{}:{}".format(hour, minute, second)
        return t

    def scriere(self, text):
        """
        Functia scrie in fisierul 'log.txt' textul primit ca si parametru.
        :param text:
        :return:
        """
        with open(self.logfn, "r") as f:
            _ = f.read()
        text = "[{} | {}] {}".format(self.data(), self.ora(), text)
        with open(self.logfn, "w") as f:
            f.write(_ + "\n" + text)

def Debug(text, tip):
    """
    Printeaza un text in cazul in care este activat modul debugging. Textul este afisat pe diferite culori, in functie
    de tipul sau:
        - informativ: culoare alba (tip = 0)
        - avertisment: culoare galbena (tip = 1)
        - eroare: culoare rosie (tip = 2)
    :param text:
    :return:
    """
    if tip == 0:
        print(colorama.Fore.WHITE, end="")
    elif tip == 1:
        print(colorama.Fore.YELLOW, end = "")
    elif tip == 2:
        print(colorama.Fore.RED, end="")

    print(text)

    print(colorama.Fore.WHITE, end="")

def Verificare_Debug():
    """
    Functie ce citeste config.cfg si returneaza True daca modul debugging este activat si False in caz contrar.
    :return:
    """
    with open(cfgfn, "r") as f:
        sett = f.read().split("\n")

    _ = ""
    for i in range(0, len(sett)):
        if "DEBUG" in sett[i]:
            _ = sett[i]
            break

    _ = _.split("=")

    return eval(_[1])
