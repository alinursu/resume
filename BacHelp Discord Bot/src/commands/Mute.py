import asyncio

import discord
from discord.ext.commands import has_permissions

from src import Globals
from src.Globals import BOT


@BOT.command()
@has_permissions(administrator=True)
async def mute(context, member=None, minutes=None, reason=None):
    """
    Da mute unui membru.
    :param member: Membrul care primeste mute (poate fi id-ul membrului sau poate avea forma "NUME#DISCRIMINATOR").
    :param minutes: Numarul de minute pentru care mute-ul va fi activ (numar intreg).
    :param reason: Motivul pentru care primeste mute-ul (parametrul trebuie scris intre ghilimele).
    """
    announcesChannel = discord.utils.get(
        discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).channels,
        name=Globals.BOT_ANNOUNCES_CHANNEL_NAME
    )

    if member == None or reason == None or member.startswith("<@!") == False:
        await announcesChannel.send("```Sintaxa comenzii \"mute\" este:\n" + \
                                   "\t!mute [member] [minutes] [reason]" + \
                                   "\nUnde:\n\t [member] este un tag al membrului (Exemplu: @Alin)\n" + \
                                   "\t [minutes] reprezinta numarul de minute pentru care mute-ul va fi activ (numar intreg)" + \
                                   "\t [reason] reprezinta motivul pentru care va primi mute (parametrul trebuie scris intre ghilimele).```")
        return
    try:
        temp = int(minutes)
    except:
        await announcesChannel.send("```Sintaxa comenzii \"mute\" este:\n" + \
                                   "\t!mute [member] [minutes] [reason]" + \
                                   "\nUnde:\n\t [member] este un tag al membrului (Exemplu: @Alin)\n" + \
                                   "\t [minutes] reprezinta numarul de minute pentru care mute-ul va fi activ (numar intreg)" + \
                                   "\t [reason] reprezinta motivul pentru care va primi mute (parametrul trebuie scris intre ghilimele).```")
        return

    guild = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID)
    members = guild.members
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    memberId = member.split("!")[1].split(">")[0]
    memberObj = None

    for member1 in members:
        if str(member1.id) == str(memberId):
            memberObj = member1
            break

    if memberObj == None:
        await announcesChannel.send("Nu am gasit membrul.")
        return

    await announcesChannel.send(
        "Am dat mute membrului " + memberObj.name + "#" + memberObj.discriminator + " timp de " + minutes + " minute."
    )

    await memberObj.add_roles(mutedRole, reason=reason)
    await memberObj.send("Ai primit mute timp de " + str(minutes) + " minute, pe motivul \"" + reason + "\".")

    await asyncio.sleep(int(minutes) * 60)

    try:
        await memberObj.remove_roles(mutedRole)
        await memberObj.send("Ti-a expirat mute-ul.")
    except:
        pass

@mute.error
async def mute_error(error, context):
    return