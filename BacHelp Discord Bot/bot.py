import discord
from discord.ext.commands import CommandNotFound, ExpectedClosingQuoteError

from src import Globals
from src.Globals import BOT
from src.data_structures import Queue, Pair, JSONFileController
from src.server_objects import Verification
from src.threads import MessagesHandlerThread, MemberJoinHandlerThread, MemberReactionHandlerThread, \
    CommandsHandlerThread, DMMessagesHandlerThread


@BOT.event
async def on_message(message):
    """
    Event handler cand cineva trimite un mesaj.
    :param message: Mesajul trimis.
    :return:
    """
    if message.content.startswith(Globals.COMMAND_PREFIX):
        await message.delete()
        Globals.COMMANDS_QUEUE.push(message)

    if message.guild == None: # Mesaj privat
        Globals.DM_MESSAGES_QUEUE.push(message)
        return

    if message.guild.id == Globals.GUILD_ID and message.author.id != Globals.BOT_ID and \
            message.channel.category.name.upper() != Globals.STAFF_CATEGORY_NAME:
        Globals.MESSAGES_QUEUE.push(message)

@BOT.event
async def on_message_edit(previousMessage, newMessage):
    """
    Event handler cand cineva modifica un mesaj (continutul, ii da pin, etc.).
    :param previousMessage: Mesajul anterior.
    :param newMessage: Mesajul nou.
    :return:
    """
    if newMessage.content.startswith(Globals.COMMAND_PREFIX):
        await newMessage.delete()
        Globals.COMMANDS_QUEUE.push(newMessage)

    if newMessage.guild == None: # Mesaj privat
        return

    if newMessage.guild.id == Globals.GUILD_ID and previousMessage.content != newMessage.content and \
            newMessage.author.id != Globals.BOT_ID and newMessage.channel.category.name.upper() != Globals.STAFF_CATEGORY_NAME:
        Globals.MESSAGES_QUEUE.push(newMessage)

@BOT.event
async def on_raw_reaction_add(event):
    """
    Event handler cand cineva reactioneaza cu un emoji la un mesaj.
    :param event: Event-ul care a declansat apelarea functiei (contine id-ul canalului, id-ul mesajului, membrul, emoji-ul, etc.)
    :return:
    """
    if event.member.id == Globals.BOT_ID:
        return

    if event.guild_id == Globals.GUILD_ID:
        channel = discord.utils.get(
            discord.utils.get(BOT.guilds, id=Globals.GUILD_ID).channels, id=event.channel_id
        )
        if channel.name.upper() == Globals.MEMBER_JOIN_CHANNEL_NAME.upper() and \
            channel.category.name.upper() == Globals.MEMBER_JOIN_CATEGORY_NAME.upper():
            pair = Pair.Pair(event.member, event.emoji)
            Globals.MEMBER_JOIN_CHANNEL_REACTIONS_QUEUE.push(pair)

@BOT.event
async def on_member_join(member):
    """
    Event handler cand cineva intra pe server.
    :param member: Membrul care intra.
    :return:
    """
    if member.guild.id == Globals.GUILD_ID:
        role = discord.utils.get(member.guild.roles, name=Globals.MEMBER_JOIN_ROLE_NAME)
        await member.add_roles(role)

        JSONFileController.addNewMember(int(member.id))

        scoreChannel = discord.utils.get(
            discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).channels, name=Globals.SCORE_CHANNEL_NAME
        )

        async for message in scoreChannel.history(limit=1):
            await message.edit(content=JSONFileController.getTop25MembersMessage())

@BOT.event
async def on_command_error(context, error):
    """
    Event handler cand apare o eroare la executarea unei comenzi.
    :param context: Contextul in care a aparut eroare.
    :param error: Eroarea.
    :return:
    """
    announcesChannel = discord.utils.get(
        discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).channels,
        name=Globals.BOT_ANNOUNCES_CHANNEL_NAME
    )

    if isinstance(error, CommandNotFound):
        await announcesChannel.send("Nu exista comanda \"" + context.message.content.split(" ")[0] + "\".")
        return
    elif isinstance(error, ExpectedClosingQuoteError):
        await announcesChannel.send("Lipsesc una sau mai multe ghilimele in comanda \"" + context.message.content + "\".")
        return

    raise error

@BOT.event
async def on_ready():
    """
    Event handler cand bot-ul porneste.
    :return:
    """

    print("Initializing...")

    await Verification.verifyObjectsExistence()

    Globals.MESSAGES_QUEUE = Queue.Queue()
    MessagesHandlerThread.startThread()

    Globals.DM_MESSAGES_QUEUE = Queue.Queue()
    DMMessagesHandlerThread.startThread()

    #Globals.MEMBERS_JOIN_QUEUE = Queue.Queue()
    #MemberJoinHandlerThread.startThread()

    Globals.MEMBER_JOIN_CHANNEL_REACTIONS_QUEUE = Queue.Queue()
    MemberReactionHandlerThread.startThread()

    Globals.COMMANDS_QUEUE = Queue.Queue()
    CommandsHandlerThread.startThread()

    print("Running...")

if __name__ == '__main__':
    BOT.run(Globals.TOKEN)