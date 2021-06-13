from ..Globals import BOT
from ..data_structures import JSONFileController

@BOT.command()
async def punctaj(context):
    """
    Afiseaza un mesaj punctajul personal.
    """
    member = context.author
    score = JSONFileController.getMemberPoints(member.id)
    await member.send("In acest moment ai " + str(score) + " puncte.")

@punctaj.error
async def punctaj_error(error, context):
    return