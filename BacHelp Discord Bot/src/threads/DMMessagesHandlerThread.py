import discord

from .. import Globals
from discord.ext import tasks

@tasks.loop(seconds=0.5)
async def messagesHandlerThread():
    """
    Loop care verifica fiecare mesaj din Queue-ul de mesaje primite in privat.
    :return:
    """
    if Globals.BOT.is_closed():
        return

    message = Globals.DM_MESSAGES_QUEUE.pop()
    if message is None:
        return

    content = "<@!" + str(message.author.id) + "> (nume: \"" + message.author.name + \
              "\") a trimis mesajul: \n" + message.content
    files = []
    for attachment in message.attachments:
        file = await attachment.to_file()
        files.append(file)

    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    channel = discord.utils.get(guild.channels, name=Globals.DM_MESSAGES_CHANNEL_NAME)
    await channel.send(content, files=files)

def startThread():
    messagesHandlerThread.start()