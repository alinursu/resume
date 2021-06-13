import discord

from src import Globals

async def createMemberJoinRole():
    """
    Creeaza un rol cu numele Globals.MEMBER_JOIN_ROLE_NAME.
    :return:
    """
    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    role = await guild.create_role(name=Globals.MEMBER_JOIN_ROLE_NAME)

    for channel in guild.channels:
        if channel.name != Globals.MEMBER_JOIN_CHANNEL_NAME:
            await channel.set_permissions(role, read_messages=False, send_messages=False)
        else:
            await channel.set_permissions(role, read_messages=True, send_messages=False)

async def createMemberRole():
    """
    Creeaza un rol cu numele Globals.MEMBER_ROLE_NAME.
    :return:
    """
    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    await guild.create_role(name=Globals.MEMBER_ROLE_NAME)

async def createMutedRole():
    """
    Creeaza un rol cu numele "Muted".
    :return:
    """
    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    role = await guild.create_role(name="Muted")
    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    for channel in guild.channels:
        await channel.set_permissions(role, speak=False, send_messages=False)