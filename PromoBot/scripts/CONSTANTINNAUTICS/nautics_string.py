autor = "Ursu Alin"
from scripts import utils

def formare_descriere(text):
    """
    Preia un text, reprezentand descrierea unui produs, si scapa de caractere speciale ("\n", "\xa0") si
    transforma textul in lista, fiecare element din lista reprezentand o propozitie din descriere.
    :param text:
    :return:
    """
    text = text.split("\xa0")

    # Scap de string-urile goale (cele fara niciun caracter sau doar cu caractere de tip spatiu)
    ok = 0
    while ok == 0:
        ok = 1
        try:
            for i in range(0, len(text)):
                if utils.verificare_string_gol(text[i]) == 1:
                    del text[i]
                    ok = 0
        except:
            pass

    # Reformez string-ul principal
    _ = ""
    for i in range(0, len(text)):
        _ = _ + text[i] + " "
    text = _

    text = text.split("\n")

    # Sterg din nou string-urile goale (cele fara niciun caracter sau doar cu caractere de tip spatiu)
    ok = 0
    while ok == 0:
        ok = 1
        try:
            for i in range(0, len(text)):
                if utils.verificare_string_gol(text[i]) == 1:
                    del text[i]
                    ok = 0
        except:
            pass

    return text

def modificare_nume_partial_imagini(nume):
    """
    Functie ce modifica numele partial ale imaginilor unui obiect. Mai exact, scapa de caracterul '#' pentru ca provoaca
    o eroare in codul HTML.
    :param nume:
    :return:
    """
    _ = nume.split("#")
    nume = _[0] + _[1]
    return nume

def formare_titlu(titlu):
    """
    Functie ce modifica titlul unui produs: scapa de caracterul '#' pentru ca provoaca o eroare in codul HTML.
    ex: "Bratara #3702" => "Bratara 3702"
    :param titlu:
    :return:
    """
    _ = titlu.split("#")
    titlu = _[0] + _[1]
    return titlu