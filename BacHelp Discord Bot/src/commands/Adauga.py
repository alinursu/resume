import discord
from discord.ext.commands import has_permissions

from .. import Globals
from ..Globals import BOT
from ..data_structures import JSONFileController


@BOT.command()
@has_permissions(administrator=True)
async def adauga(context, member=None, numberOfPoints=None):
    """
    Adauga puncte unui membru.
    :param member: Membrul caruia i se ofera puncte (poate fi de forma "@Alin" (tag) sau "tuturor").
    :param numberOfPoints: Numarul de puncte oferite.
    """
    announcesChannel = discord.utils.get(
        discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).channels,
        name=Globals.BOT_ANNOUNCES_CHANNEL_NAME
    )

    if member == None or numberOfPoints == None or (member.lower() != "tuturor" and member.startswith("<@!") == False):
        await announcesChannel.send("```Sintaxa comenzii \"adauga\" este:\n" + \
                                   "\t!adauga [member] [points]" + \
                                   "\nUnde:\n\t [member] este tag-ul unui membru (Exemplu: @Alin)\n" + \
                                   "\t\t[member] poate fi si \"tuturor\" pentru a oferi un numar de puncte tuturor membrilor de pe server\n" + \
                                   "\t [points] reprezinta numarul de puncte (numar intreg)```")
        return

    try:
        temp = int(numberOfPoints)
    except:
        await announcesChannel.send("```Sintaxa comenzii \"adauga\" este:\n" + \
                                   "\t!adauga [member] [points]" + \
                                   "\nUnde:\n\t [member] este tag-ul unui membru (Exemplu: @Alin)\n" + \
                                   "\t\t[member] poate fi si \"tuturor\" pentru a oferi un numar de puncte tuturor membrilor de pe server\n" + \
                                   "\t [points] reprezinta numarul de puncte (numar intreg)```")
        return


    # Adaug puncte tuturor
    if member.lower() == "tuturor":
        members = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).members
        for member in members:
            answer = JSONFileController.modifyMemberPoints(int(member.id), int(numberOfPoints))
            if answer == False:
                JSONFileController.addNewMember(int(member.id))
                JSONFileController.modifyMemberPoints(int(member.id), int(numberOfPoints))
        await announcesChannel.send("Am adaugat " + numberOfPoints + " puncte tuturor membrilor.")

        # Fac update mesajului cu topul punctajelor
        scoreChannel = discord.utils.get(
            discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).channels, name=Globals.SCORE_CHANNEL_NAME
        )
        async for message in scoreChannel.history(limit=1):
            await message.edit(content=JSONFileController.getTop25MembersMessage())

        return

    # Adaug puncte unui membru dat
    members = discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).members
    memberId = member.split("!")[1].split(">")[0]
    memberObj = None

    for member1 in members:
        if str(member1.id) == str(memberId):
            memberObj = member1
            break

    if memberObj == None:
        await announcesChannel.send("Nu am gasit niciun membru cu numele \"" + member + "\".")
        return

    answer = JSONFileController.modifyMemberPoints(int(memberObj.id), int(numberOfPoints))
    if answer == False:
        JSONFileController.addNewMember(int(memberObj.id))
        JSONFileController.modifyMemberPoints(int(memberObj.id), int(numberOfPoints))
    await announcesChannel.send("Am adaugat " + numberOfPoints + " puncte membrului \"" + (
        memberObj.name if memberObj.nick == None else memberObj.nick
    ) + "\".")

    await memberObj.send("Ai primit " + numberOfPoints + " puncte.")

    # Fac update mesajului cu topul punctajelor
    scoreChannel = discord.utils.get(
        discord.utils.get(Globals.BOT.guilds, id=Globals.GUILD_ID).channels, name=Globals.SCORE_CHANNEL_NAME
    )
    async for message in scoreChannel.history(limit=1):
        await message.edit(content=JSONFileController.getTop25MembersMessage())

@adauga.error
async def adauga_error(error, context):
    return