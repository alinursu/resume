import discord
from discord.ext.commands import has_permissions

from src import Globals
from src.Globals import BOT
from src.data_structures import JSONFileController


@BOT.command()
@has_permissions(administrator=True)
async def avertisment(context, member=None, reason=None):
    """
    Da avertisment unui membru.
    :param member: Membrul care primeste avertisment (sub forma de tag; exemplu: @Alin).
    :param reason: Motivul pentru care primeste avertismentul (parametrul trebuie scris intre ghilimele).
    """
    announcesChannel = discord.utils.get(
        discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).channels,
        name=Globals.BOT_ANNOUNCES_CHANNEL_NAME
    )

    if member == None or reason == None or member.startswith("<@!") == False:
        await announcesChannel.send("```Sintaxa comenzii \"avertisment\" este:\n" + \
                                   "\t!avertisment [member] [reason]" + \
                                   "\nUnde:\n\t [member] este un tag al membrului (Exemplu: @Alin)\n" + \
                                   "\t [reason] reprezinta motivul pentru care va primi avertisment (parametrul trebuie scris intre ghilimele).```")
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

    JSONFileController.modifyMemberWarnings(memberObj.id)
    await memberObj.send("Ai primit un avertisment pe motivul \"" + reason + "\".")
    await announcesChannel.send("Am dat avertisment membrului " + memberObj.name + "#" + memberObj.discriminator + ".")

    numberOfWarnings = JSONFileController.getMemberWarnings(memberObj.id)
    if numberOfWarnings >= 5:
        try:
            await memberObj.ban(reason="Ai primit ban deoarece ai primit prea multe avertismente.")
        except:
            pass
    elif numberOfWarnings >= 3:
        try:
            await memberObj.kick(reason="Ai primit kick deoarece ai primit prea multe avertismente.")
        except:
            pass

@avertisment.error
async def avertisment_error(error, context):
    return