import os
import sys

import discord

from src import Globals


def readJSONFile(fileName):
    """
    Citeste fisierul JSON si creeaza un dictionar cu datele din acesta.
    :return: Dictionarul creat.
    """
    currentDirectory = os.getcwd()
    slash = "/" if sys.platform.lower().startswith("linux") else "\\"
    dictionary = {}

    with open(currentDirectory + slash + "data" + slash + fileName, "r") as file:
        for line in file:
            if line.strip() != "" and line.strip() != "{" and line.strip() != "}":
                splittedLine = line.strip().split(":")
                if "," in splittedLine[1]:
                    dictionary[splittedLine[0].replace("\"", "")] = splittedLine[1].split(",")[0].replace("\"", "")
                else:
                    dictionary[splittedLine[0].replace("\"", "")] = splittedLine[1].replace("\"", "")

    file.close()
    return dictionary

def modifyJSONFile(fileName, dictionary):
    """
    Sterge continutul actual al fisierului JSON si adauga datele din parametrul dat.
    :param dictionary: Datele care vor fi adaugate in fisier.
    :return:
    """
    currentDirectory = os.getcwd()
    slash = "/" if sys.platform.lower().startswith("linux") else "\\"

    with open(currentDirectory + slash + "data" + slash + fileName, "w") as file:
        file.write("{\n")

        for i in range(0, len(dictionary.keys()) - 1):
            key = list(dictionary.keys())[i]
            file.write("\t\"" + str(key) + "\":\"" + str(dictionary[key]) + "\",\n")

        key = list(dictionary.keys())[len(dictionary.keys())-1]
        file.write("\t\"" + str(key) + "\":\"" + str(dictionary[key]) + "\"\n")

        file.write("}")

    file.close()

def addNewMember(memberId):
    """
    Adauga un nou membru in fisierul JSON.
    :param memberId: Id-ul membrului care va fi adaugat (de tip int sau str).
    :return: True, daca membrul a fost adaugat; False, altfel
    """
    contentDictionary = readJSONFile(Globals.SCORE_JSON_FILE_NAME)
    if str(memberId) not in contentDictionary.keys():
        contentDictionary[str(memberId)] = "0"
        modifyJSONFile(Globals.SCORE_JSON_FILE_NAME, contentDictionary)

    contentDictionary = readJSONFile(Globals.WARNING_FILE_NAME)
    if str(memberId) not in contentDictionary.keys():
        contentDictionary[str(memberId)] = "0"
        modifyJSONFile(Globals.WARNING_FILE_NAME, contentDictionary)
        return True

    return False

def modifyMemberPoints(memberId, points):
    """
    Modifica punctele membrului cu id-ul memberId, adaugand punctajului sau actual numarul reprezentat de points.
    :param memberId: Id-ul membrului caruia i se va modifica punctajul.
    :param points: Numarul cu care se va modifica.
    :return: True, daca punctajul a fost modificat; False, altfel (membrul nu este inregistrat in JSON).
    """
    contentDictionary = readJSONFile(Globals.SCORE_JSON_FILE_NAME)
    if str(memberId) not in contentDictionary.keys():
        return False

    contentDictionary[str(memberId)] = str(int(contentDictionary[str(memberId)]) + points)
    modifyJSONFile(Globals.SCORE_JSON_FILE_NAME, contentDictionary)
    return True

def getMemberPoints(memberId):
    """
    Cauta in fisierul JSON punctajul unui membru.
    :param memberId: Id-ul membrului (de tip int sau str).
    :return: Punctajul membrului, daca acesta se afla in fisier; 0, altfel
    """
    contentDictionary = readJSONFile(Globals.SCORE_JSON_FILE_NAME)
    if str(memberId) not in contentDictionary.keys():
        return 0

    return contentDictionary[str(memberId)]

def getTop25Members():
    """
    Cauta in fisierul JSON 25 de membri cu punctajul cel mai mare.
    :return: Un dictionar cu cei 25 de membri cu cele mai mari punctaje.
    """
    contentDictionary = readJSONFile(Globals.SCORE_JSON_FILE_NAME)

    keys = list(contentDictionary.keys())
    values = list(contentDictionary.values())
    for i in range(0, len(keys)):
        for j in range(0, len(keys)):
            if values[i] > values[j]:
                tempKey = keys[i]
                tempValue = values[i]
                keys[i] = keys[j]
                values[i] = values[j]
                keys[j] = tempKey
                values[j] = tempValue

    dictionary = {}
    for i in range(0, min(25, len(keys))):
        dictionary[keys[i]] = values[i]

    return dictionary

def getTop25MembersMessage():
    """
    :return: Un mesaj (str) continand top 25 cele mai mari punctaje.
    """
    top25 = getTop25Members()
    message = "```Topul punctajelor:\n"
    index = 0
    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    for key in top25.keys():
        index = index + 1
        try:
            member = discord.utils.get(guild.members, id=int(key))
            message = message + "\t" + str(index) + ". " + (
                    member.name if member.nick == None else member.nick
                ) + " -> " + str(top25[key]) + "\n"
        except:
            index = index - 1
    message = message + "```"

    return message

def modifyMemberWarnings(memberId):
    """
    Modifica numarul de avertismente ale membrului cu id-ul memberId, adaugand inca unul.
    :param memberId: Id-ul membrului caruia i se va da un avertisment.
    :return: True, daca numarul de avertismente a fost modificat; False, altfel (membrul nu este inregistrat in JSON).
    """
    contentDictionary = readJSONFile(Globals.WARNING_FILE_NAME)
    if str(memberId) not in contentDictionary.keys():
        return False

    contentDictionary[str(memberId)] = str(int(contentDictionary[str(memberId)]) + 1)
    modifyJSONFile(Globals.WARNING_FILE_NAME, contentDictionary)
    return True

def getMemberWarnings(memberId):
    """
    Cauta in fisierul JSON numarul de avertismente ale unui membru.
    :param memberId: Id-ul membrului (de tip int sau str).
    :return: Numarul de avertismente ale membrului, daca acesta se afla in fisier; 0, altfel
    """
    contentDictionary = readJSONFile(Globals.WARNING_FILE_NAME)
    if str(memberId) not in contentDictionary.keys():
        return 0

    return contentDictionary[str(memberId)]