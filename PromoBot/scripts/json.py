autor = "Ursu Alin"
import os
import sys

if sys.platform == "Windows":
    slash = "\\"
else:
    slash = "/"
path = os.getcwd() + slash
jsonpath = path + "bin" + slash + "json" + slash

class JsonCommunicator:
    """
    Clasa folosita pentru a crea un obiect ce va "comunica" cu fisierele json din program (le va citi si transforma
    intr-o variabila de tip dictionar).
    """
    def __init__(self, filename):
        self.fn = filename
        self.data = eval(self.citire_fisier())

    def citire_fisier(self):
        os.chdir(jsonpath)
        with open(self.fn, 'r') as f:
            _ = f.read()
        os.chdir(path)
        return _

    def continut_fisier(self):
        return self.data

