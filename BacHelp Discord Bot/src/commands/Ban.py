import discord
from discord.ext.commands import has_permissions

from src import Globals
from src.Globals import BOT


@BOT.command()
@has_permissions(administrator=True)
async def ban(context, member=None, reason=None):
    """
    Da ban unui membru.
    :param member: Membrul care primeste ban (sub forma de tag; exemplu: @Alin).
    :param reason: Motivul pentru care primeste ban-ul (parametrul trebuie scris intre ghilimele).
    """
    announcesChannel = discord.utils.get(
        discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).channels,
        name=Globals.BOT_ANNOUNCES_CHANNEL_NAME
    )

    if member == None or reason == None or member.startswith("<@!") == False:
        await announcesChannel.send("```Sintaxa comenzii \"ban\" este:\n" + \
                                   "\t!ban [member] [reason]" + \
                                   "\nUnde:\n\t [member] este un tag al membrului (Exemplu: @Alin).\n" + \
                                   "\t [reason] reprezinta motivul pentru care va primi ban (parametrul trebuie scris intre ghilimele).```")
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
        await memberObj.ban(reason=reason)
    except:
        pass
    await announcesChannel.send("Am dat ban membrului " + memberObj.name + "#" + memberObj.discriminator + " pe motivul \"" + reason + "\".")

@ban.error
async def ban_error(error, context):
    return