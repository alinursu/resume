import discord
from discord.ext import tasks

from src import Globals
from src.data_structures import JSONFileController


@tasks.loop(seconds=0.5)
async def memberJoinHandlerThread():
    """
    Loop care face actiuni pentru fiecare membru din Globals.MEMBERS_JOIN_QUEUE.
    :return:
    """
    if Globals.BOT.is_closed():
        return

    member = Globals.MEMBERS_JOIN_QUEUE.pop()
    if member is None:
        return

    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    role = discord.utils.get(guild.roles, name=Globals.MEMBER_JOIN_ROLE_NAME)
    try:
        await member.add_roles(role)
    except:
        await member.author.add_roles(role)

    JSONFileController.addNewMember(int(member.id))

    scoreChannel = discord.utils.get(
        discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).channels, name=Globals.SCORE_CHANNEL_NAME
    )
    async for message in scoreChannel.history(limit=1):
        await message.edit(content=JSONFileController.getTop25MembersMessage())

def startThread():
    memberJoinHandlerThread.start()