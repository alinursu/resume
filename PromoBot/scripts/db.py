autor = "Ursu Alin"
import sqlite3
import os
import sys
import datetime

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
datapath = path + "bin" + slash + "data" + slash

def data_actuala():
    """
    Functie ce returneaza un string, reprezentand data actuala (format: "ZI-LUNA-AN").
    :return:
    """
    now = datetime.datetime.now()
    data = "{}-{}-{}"
    if now.day >= 10:
        zi = str(now.day)
    else:
        zi = "0" + str(now.day)

    if now.month >= 10:
        luna = str(now.month)
    else:
        luna = "0" + str(now.month)

    data = data.format(zi, luna, str(now.year))
    return data

def formare_int_pret(pret):
    """
    Functie ce converteste un string special intr-un intreg.
    ex: "1.299,99" => 1300
    :param pret:
    :return:
    """
    pret = pret.split(".")

    if len(pret) == 1:
        # Pret < 1000 (ex: 299,99)
        pret = int(pret[0].split(",")[0]) + 1
        return pret
    else:
        # Pret > 1000 (ex: 1.299,99)
        _ = pret[0]
        pret = int(pret[1].split(",")[0]) + 1
        pret = int(_) * 1000 + pret
        return pret

def alegere_pretul_minim(lista):
    """
    Functie ce alege pretul minim dintr-o lista de tip dictionar.
    :param lista:
    :return:
    """
    minim = 99999999
    for i in range(0, len(lista)):
        if lista[i]["pret"] < minim:
            minim = lista[i]["pret"]

    for i in range(0, len(lista)):
        if lista[i]["pret"] == minim:
            return lista[i]

def comparare_data_actuala_cu_ultima(data):
    """
    Functie ce compara data actuala cu ultima data la care apare link-ul in baza de date si returneaza valoarea 1,
    daca diferenta dintre cele doua este de cel putin 3 zile, si 0 in caz contrar.
    :param data:
    :return:
    """
    data = data.split("-")
    actuala = data_actuala().split("-")
    if abs(int(data[0]) - int(actuala[0])) >= 3:
        return 1
    elif int(actuala[1]) > int(data[1]) and int(actuala[2]) >= int(data[2]):
        return 1
    else:
        return 0

class Database:
    """
    Clasa folosita pentru a comunica cu baza de date "/bin/data/db.db/"
    """
    def __init__(self, table):
        self.table = table
        self.dbname = "db.db"

        self.comanda_adaugare = "INSERT INTO {}(link, pret, data) VALUES ('%s', %d, '%s')"
        self.comanda_cautare = "SELECT * FROM {}"
    def initializare_conexiune(self):
        """
        Functie ce initializeaza conexiunea si cursorul folosit pentru a executa comenzi.
        :return:
        """
        os.chdir(datapath)
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
        os.chdir(path)
    def inchidere_conexiune(self):
        """
        Functie ce inchide conexiunea cu baza de date.
        :return:
        """
        self.conn.close()
    def adaugare_date(self, data):
        """
        Functie ce adauga date intr-o tabela aleasa la initializarea obiectului de tip DATABASE.
        :param data:
        :return:
        """
        self.cursor.execute(self.comanda_adaugare.format(self.table) % (data["link"], formare_int_pret(data["pret"]), data_actuala()))
        self.conn.commit()
    def adaugare_date_2(self, data):
        """
        Functie ce adauga date intr-o tabela aleasa la initializarea obiectului de tip DATABASE.
        :param data:
        :return:
        """
        self.cursor.execute(self.comanda_adaugare.format(self.table) % (data["link"], data["pret"], data_actuala()))
        self.conn.commit()
    def cautare_date_link(self, link):
        """
        Functie ce returneaza o lista cu perechi de dictionare continand data si pretul la care a mai fost gasit.
        :param link:
        :return:
        """
        self.cursor.execute(self.comanda_cautare.format(self.table))
        d = self.cursor.fetchall()
        l = []
        for i in range(0, len(d)):
            if d[i][0] == link:
                l.append({"data":d[i][2], "pret":d[i][1]})

        return l
    def cautare_ultima_data(self, link):
        """
        Functie ce cauta ultima data in care a fost salvat un pret legat de un anumit link. Daca nu exista nicio data,
        returneaza valoarea 0.
        :return:
        """
        self.cursor.execute(self.comanda_cautare.format(self.table))
        d = self.cursor.fetchall()
        data = "0-0-0"
        for i in range(0, len(d)):
            if d[i][0] == link:
                if int(d[i][2].split("-")[0]) > int(data.split("-")[0]) and int(d[i][2].split("-")[1]) >= int(data.split("-")[1]) and int(d[i][2].split("-")[2]) >= int(data.split("-")[2]):
                    data = d[i][2]
        if data == "0-0-0":
            return 0
        else:
            return data