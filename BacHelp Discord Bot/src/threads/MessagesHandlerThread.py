from .. import Globals
from discord.ext import tasks
import unidecode

def isForbiddenWord(word):
    """
    Verifica daca un cuvant este vulgar.
    :param word: Cuvantul, in format string.
    :return:
    """
    listOfForbiddenWords = ["lista", "cuvintelor", "vulgare"]
    if word in listOfForbiddenWords:
        return True

    return False

async def sendBotAnnounce(message):
    """
    Trimite un mesaj predefinit pe canalul cu numele Globals.BOT_ANNOUNCES_CHANNEL_NAME.
    :param message: Mesajul pentru care s-a apelat functia (de tipul discord.Message).
    :return:
    """
    server = Globals.BOT.get_guild(Globals.GUILD_ID)
    temp = [ch for ch in server.channels if ch.name == Globals.BOT_ANNOUNCES_CHANNEL_NAME]
    channel = temp[0]
    date = message.created_at.replace(hour=message.created_at.hour+3)
    textMessage = "----\nAm detectat cuvinte vulgare in mesajul \"" + message.content + "\" trimis de <@!" + \
        str(message.author.id) + "> (nume:\"" + message.author.name + "\") la data " + str(date) + ", pe canalul \"" + \
                  message.channel.name + "\" (categoria \"" +  \
                  message.channel.category.name +"\").\n----"
    await channel.send(textMessage)


@tasks.loop(seconds=0.5)
async def messagesHandlerThread():
    """
    Loop care verifica fiecare mesaj din Queue-ul de mesaje.
    :return:
    """
    if Globals.BOT.is_closed():
        return

    message = Globals.MESSAGES_QUEUE.pop()
    if message is None:
        return

    messageStr = unidecode.unidecode(message.content)
    messageStr.replace(",", "")
    messageStr.replace(".", "")
    messageStr.replace("!", "")
    messageStr.replace("?", "")
    messageStr.replace(":", "")
    messageStr.replace(";", "")
    listOfWords = messageStr.split(" ")

    for word in listOfWords:
        if isForbiddenWord(word):
            await sendBotAnnounce(message)
            try:
                await message.delete()
            except:
                pass
            break

def startThread():
    messagesHandlerThread.start()