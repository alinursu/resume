import os
import sys

import discord

from . import Channels, Roles
from .. import Globals
from ..data_structures import JSONFileController


def verifyBotAnnouncesChannelExistence():
    """
    Verifica daca exista un canal cu numele Globals.BOT_ANNOUNCES_CHANNEL_NAME, in categoria Globals.BOT_CATEGORY_NAME.
    :return: True, daca exista; False, atlfel
    """
    try:
        guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
        channel = discord.utils.get(guild.channels, name=Globals.BOT_ANNOUNCES_CHANNEL_NAME)

        if channel == None:
            return False

        if channel.category.name.upper() != Globals.BOT_CATEGORY_NAME:
            return False

        return True
    except:
        print("exception")
        return False

def verifyMemberJoinChannelExistence():
    """
        Verifica daca exista un canal cu numele Globals.MEMBER_JOIN_CHANNEL_NAME, in categoria Globals.MEMBER_JOIN_CATEGORY_NAME.
        :return: True, daca exista; False, atlfel
        """
    try:
        guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
        channel = discord.utils.get(guild.channels, name=Globals.MEMBER_JOIN_CHANNEL_NAME)

        if channel == None:
            return False
        if channel.category.name != Globals.MEMBER_JOIN_CATEGORY_NAME:
            return False

        return True
    except:
        return False


def verifyMemberJoinRoleExistence():
    """
    Verifica daca exista un rol cu numele Globals.MEMBER_JOIN_ROLE_NAME.
    :return: True, daca exista; False, atlfel
    """
    try:
        guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
        role = discord.utils.get(guild.roles, name=Globals.MEMBER_JOIN_ROLE_NAME)

        if role == None:
            return False

        return True
    except:
        return False


def verifyMemberRoleExistence():
    """
    Verifica daca exista un rol cu numele Globals.MEMBER_ROLE_NAME.
    :return: True, daca exista; False, atlfel
    """
    try:
        guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
        role = discord.utils.get(guild.roles, name=Globals.MEMBER_ROLE_NAME)

        if role == None:
            return False

        return True
    except:
        return False

def verifyMutedRoleExistence():
    """
    Verifica daca exista un rol cu numele "Muted".
    :return: True, daca exista; False, atlfel
    """
    try:
        guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
        role = discord.utils.get(guild.roles, name="Muted")

        if role == None:
            return False

        return True
    except:
        return False

def verifyScoreJsonFileExistence():
    """
    Verifica daca exista fisierul Globals.SCORE_JSON_FILE_NAME in path-ul "<CWD>/data/".
    :return: True, daca fisierul exista; False, altfel.
    """
    currentDirectory = os.getcwd()
    slash = "/" if sys.platform.lower().startswith("linux") else "\\"

    return os.path.isfile(currentDirectory + slash + "data" + slash + Globals.SCORE_JSON_FILE_NAME)


def createScoreJsonFile():
    """
    Creeaza fisierul Globals.SCORE_JSON_FILE_NAME in path-ul "<CWD>/data/.
    :return:
    """
    currentDirectory = os.getcwd()
    slash = "/" if sys.platform.lower().startswith("linux") else "\\"

    with open(currentDirectory + slash + "data" + slash + Globals.SCORE_JSON_FILE_NAME, "w") as file:
        file.write("{\n")
        members = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).members
        for i in range(0, len(members) - 1):
            file.write("\t\"" + str(members[i].id) + "\":\"0\",\n")
        file.write("\t\"" + str(members[len(members) - 1].id) + "\":\"0\"\n")
        file.write("}")

    file.close()

def verifyWarningJsonFileExistence():
    """
    Verifica daca exista fisierul Globals.WARNING_FILE_NAME in path-ul "<CWD>/data/".
    :return: True, daca fisierul exista; False, altfel.
    """
    currentDirectory = os.getcwd()
    slash = "/" if sys.platform.lower().startswith("linux") else "\\"

    return os.path.isfile(currentDirectory + slash + "data" + slash + Globals.WARNING_FILE_NAME)


def createWarningJsonFile():
    """
    Creeaza fisierul Globals.WARNING_FILE_NAME in path-ul "<CWD>/data/.
    :return:
    """
    currentDirectory = os.getcwd()
    slash = "/" if sys.platform.lower().startswith("linux") else "\\"

    with open(currentDirectory + slash + "data" + slash + Globals.WARNING_FILE_NAME, "w") as file:
        file.write("{\n")
        members = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).members
        for i in range(0, len(members) - 1):
            file.write("\t\"" + str(members[i].id) + "\":\"0\",\n")
        file.write("\t\"" + str(members[len(members) - 1].id) + "\":\"0\"\n")
        file.write("}")

    file.close()

def verifyScoreChannelExistence():
    """
    Verifica daca exista un canal cu numele Globals.SCORE_CHANNEL_NAME, in categoria Globals.BOT_CATEGORY_NAME.
    :return: True, daca exista; False, atlfel
    """
    try:
        guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
        channel = discord.utils.get(guild.channels, name=Globals.SCORE_CHANNEL_NAME)

        if channel == None:
            return False
        if channel.category.name.upper() != Globals.BOT_CATEGORY_NAME:
            return False

        return True
    except:
        return False

def verifyDMMessagesChannelExistence():
    """
    Verifica daca exista un canal cu numele Globals.DM_MESSAGES_CHANNEL_NAME, in categoria Globals.BOT_CATEGORY_NAME.
    :return: True, daca exista; False, altfel
    """
    try:
        guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
        channel = discord.utils.get(guild.channels, name=Globals.DM_MESSAGES_CHANNEL_NAME)

        if channel == None:
            return False
        if channel.category.name.upper() != Globals.BOT_CATEGORY_NAME:
            return False

        return True
    except:
        return False

async def verifyObjectsExistence():
    """
    Verifica daca obiectele de care bot-ul are nevoie exista pe server (roluri, canale, etc.). Daca nu exista, le creeaza.
    :return:
    """
    if verifyScoreJsonFileExistence() == False:
        createScoreJsonFile()

    if verifyWarningJsonFileExistence() == False:
        createWarningJsonFile()

    if verifyMutedRoleExistence() == False:
        await Roles.createMutedRole()

    if verifyMemberRoleExistence() == False:
        await Roles.createMemberRole()

    if verifyMemberJoinRoleExistence() == False:
        await Roles.createMemberJoinRole()

    if verifyBotAnnouncesChannelExistence() == False:
        await Channels.createBotAnnouncesChannel()

    if verifyScoreChannelExistence() == False:
        await Channels.createScoreChannel()

    if verifyMemberJoinChannelExistence() == False:
        await Channels.createMemberJoinChannel()

    if verifyDMMessagesChannelExistence() == False:
        await Channels.createDMMessagesChannel()
