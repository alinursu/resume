import discord

from .. import Globals
from ..Globals import BOT
from ..data_structures import JSONFileController

@BOT.command()
async def unmute(context, member=None):
    """
    Scoate mute-ul unui membru.
    :param member: Membrul care primeste unmute (sub forma de tag; exemplu: @Alin).
    """
    announcesChannel = discord.utils.get(
        discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).channels,
        name=Globals.BOT_ANNOUNCES_CHANNEL_NAME
    )

    if member == None:
        await announcesChannel.send("```Sintaxa comenzii \"unmute\" este:\n" + \
                                    "\t!unmute [member]" + \
                                    "\nUnde:\n\t [member] este un tag al membrului (Exemplu: @Alin).```")
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

    if mutedRole not in memberObj.roles:
        await announcesChannel.send("Membrul " + memberObj.name + "#" + memberObj.discriminator + " nu are mute.")
        return

    try:
        await memberObj.remove_roles(mutedRole)
        await announcesChannel.send("Am scos mute-ul membrului " + memberObj.name + "#" + memberObj.discriminator + ".")
        await memberObj.send("Ti-a expirat mute-ul.")
    except:
        pass

@unmute.error
async def unmute_error(error, context):
    return