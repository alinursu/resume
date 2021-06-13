import discord
from discord.ext import tasks

from src import Globals
from src.commands.Adauga import adauga, adauga_error
from src.commands.Punctaj import punctaj, punctaj_error
from src.commands.Kick import kick, kick_error
from src.commands.Ban import ban, ban_error
from src.commands.Avertisment import avertisment, avertisment_error
from src.commands.Mute import mute, mute_error
from src.commands.Unmute import unmute, unmute_error


@tasks.loop(seconds=0.5)
async def commandsHandlerThread():
    """
    Loop care face actiuni pentru fiecare comanda din Globals.COMMANDS_QUEUE.
    :return:
    """
    if Globals.BOT.is_closed():
        return

    command = Globals.COMMANDS_QUEUE.pop()
    if command is None:
        return

    try:
        await Globals.BOT.process_commands(command)
    except:
        pass
    return

def startThread():
    commandsHandlerThread.start()
