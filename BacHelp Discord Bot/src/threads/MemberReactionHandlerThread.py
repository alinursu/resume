import discord
from discord.ext import tasks

from src import Globals
from src.data_structures import JSONFileController


@tasks.loop(seconds=0.5)
async def memberReactionHandlerThread():
    """
    Loop care face actiuni pentru fiecare reactie din din Globals.MEMBER_JOIN_CHANNEL_REACTIONS_QUEUE.
    :return:
    """
    if Globals.BOT.is_closed():
        return

    pair = Globals.MEMBER_JOIN_CHANNEL_REACTIONS_QUEUE.pop()
    if pair is None:
        return

    if pair.getValue().name == "👍":
        member = pair.getKey()
        guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)

        newcomerRole = discord.utils.get(guild.roles, name=Globals.MEMBER_JOIN_ROLE_NAME)
        studentRole = discord.utils.get(guild.roles, name=Globals.MEMBER_ROLE_NAME)

        if studentRole != None:
            await member.add_roles(studentRole)
        if newcomerRole != None:
            await member.remove_roles(newcomerRole)

        JSONFileController.addNewMember(member.id)
    elif pair.getValue().name == "👎":
        member = pair.getKey()
        try:
            await member.kick(reason="Pentru a putea participa, trebuie sa accepti regulamentul.")
        except:
            pass

def startThread():
    memberReactionHandlerThread.start()