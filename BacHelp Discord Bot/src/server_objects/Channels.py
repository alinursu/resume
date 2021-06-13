import discord

from src import Globals
from src.data_structures import JSONFileController


async def createBotAnnouncesChannel():
    """
    Creeaza un canal text cu numele Globals.BOT_ANNOUNCES_CHANNEL_NAME, sub categoria Globals.BOT_CATEGORY_NAME.
    :return:
    """
    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    temp = [category for category in guild.categories if category.name.upper() == Globals.BOT_CATEGORY_NAME]
    if len(temp) == 0:
        category = await guild.create_category(name=Globals.BOT_CATEGORY_NAME)
    else:
        category = temp[0]

    channel = await category.create_text_channel(Globals.BOT_ANNOUNCES_CHANNEL_NAME)
    await channel.set_permissions(discord.utils.get(category.guild.roles, name="@everyone"),
                                  read_messages=False,
                                  send_messages=False)

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="STAFF"),
                                      read_messages=True,
                                      send_messages=True)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Moderator"),
                                      read_messages=True,
                                      send_messages=True)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Mentor MATE"),
                                      read_messages=True,
                                      send_messages=True)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Mentor INFO"),
                                      read_messages=True,
                                      send_messages=True)
    except:
        pass

async def createMemberJoinChannel():
    """
    Creeaza un canal text cu numele Globals.MEMBER_JOIN_CHANNEL_NAME, sub categoria Globals.MEMBER_JOIN_CATEGORY_NAME.
    :return:
    """
    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    temp = [category for category in guild.categories if category.name == Globals.MEMBER_JOIN_CATEGORY_NAME]
    if len(temp) == 0:
        category = await guild.create_category(name=Globals.MEMBER_JOIN_CATEGORY_NAME)
    else:
        category = temp[0]

    channel = await category.create_text_channel(Globals.MEMBER_JOIN_CHANNEL_NAME)
    await channel.set_permissions(discord.utils.get(category.guild.roles, name="@everyone"),
                                  read_messages=False,
                                  send_messages=False)

    await channel.set_permissions(discord.utils.get(category.guild.roles, name=Globals.MEMBER_JOIN_ROLE_NAME),
                                  read_messages=True,
                                  send_messages=False)

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="STAFF"),
                                      read_messages=True,
                                      send_messages=False)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Moderator"),
                                      read_messages=True,
                                      send_messages=False)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Mentor MATE"),
                                      read_messages=True,
                                      send_messages=False)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Mentor INFO"),
                                      read_messages=True,
                                      send_messages=False)
    except:
        pass

    message = await channel.send(Globals.RULES_MESSAGE)
    await message.add_reaction("👍")
    await message.add_reaction("👎")

async def createScoreChannel():
    """
    Creeaza un canal text cu numele Globals.SCORE_CHANNEL_NAME, sub categoria Globals.BOT_CATEGORY_NAME.
    :return:
    """
    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    temp = [category for category in guild.categories if category.name == Globals.BOT_CATEGORY_NAME]
    if len(temp) == 0:
        category = await guild.create_category(name=Globals.BOT_CATEGORY_NAME)
    else:
        category = temp[0]

    channel = await category.create_text_channel(Globals.SCORE_CHANNEL_NAME)
    await channel.set_permissions(discord.utils.get(category.guild.roles, name="@everyone"),
                                  read_messages=False,
                                  send_messages=False)

    await channel.set_permissions(discord.utils.get(category.guild.roles, name=Globals.MEMBER_ROLE_NAME),
                                  read_messages=True,
                                  send_messages=False)

    await channel.set_permissions(discord.utils.get(category.guild.roles, name="Muted"),
                                  read_messages=True,
                                  send_messages=False)

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="STAFF"),
                                      read_messages=True,
                                      send_messages=False)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Moderator"),
                                      read_messages=True,
                                      send_messages=False)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Mentor MATE"),
                                      read_messages=True,
                                      send_messages=False)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Mentor INFO"),
                                      read_messages=True,
                                      send_messages=False)
    except:
        pass

    await channel.send(JSONFileController.getTop25MembersMessage())

async def createDMMessagesChannel():
    """
    Creeaza un canal text cu numele Globals.DM_MESSAGES_CHANNEL_NAME, sub categoria Globals.BOT_CATEGORY_NAME.
    :return:
    """
    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    temp = [category for category in guild.categories if category.name.upper() == Globals.BOT_CATEGORY_NAME.upper()]
    if len(temp) == 0:
        category = await guild.create_category(name=Globals.BOT_CATEGORY_NAME)
    else:
        category = temp[0]

    channel = await category.create_text_channel(Globals.DM_MESSAGES_CHANNEL_NAME)
    await channel.set_permissions(discord.utils.get(category.guild.roles, name="@everyone"),
                                  read_messages=False,
                                  send_messages=False)

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="STAFF"),
                                      read_messages=True,
                                      send_messages=True)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Moderator"),
                                      read_messages=True,
                                      send_messages=True)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Mentor MATE"),
                                      read_messages=True,
                                      send_messages=True)
    except:
        pass

    try:
        await channel.set_permissions(discord.utils.get(category.guild.roles, name="Mentor INFO"),
                                      read_messages=True,
                                      send_messages=True)
    except:
        pass
