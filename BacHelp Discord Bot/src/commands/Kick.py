import discord
from discord.ext.commands import has_permissions

from src import Globals
from src.Globals import BOT


@BOT.command()
@has_permissions(administrator=True)
async def kick(context, member=None, reason=None):
    """
    Da kick unui membru.
    :param member: Membrul care primeste kick (sub forma de tag; exemplu: @Alin).
    :param reason: Motivul pentru care primeste kick-ul (parametrul trebuie scris intre ghilimele).
    """
    announcesChannel = discord.utils.get(
        discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).channels,
        name=Globals.BOT_ANNOUNCES_CHANNEL_NAME
    )

    if member == None or reason == None or member.startswith("<@!") == False:
        await announcesChannel.send("```Sintaxa comenzii \"kick\" este:\n" + \
                                   "\t!kick [member] [reason]" + \
                                   "\nUnde:\n\t [member] este un tag al membrului (Exemplu: @Alin).\n" + \
                                   "\t [reason] reprezinta motivul pentru care va primi kick (parametrul trebuie scris intre ghilimele).```")
        return

    members = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).members

    memberId = member.split("!")[1].split(">")[0]
    memberObj = None

    for member1 in members:
        if str(member1.id) == str(memberId):
            memberObj = member1
            break

    if memberObj == None:
        await announcesChannel.send("Nu am gasit membrul.")
        return

    try:
        await memberObj.kick(reason=reason)
    except:
        pass
    await announcesChannel.send("Am dat kick membrului " + memberObj.name + "#" + memberObj.discriminator + " pe motivul \"" + reason + "\".")

@kick.error
async def kick_error(error, context):
    return