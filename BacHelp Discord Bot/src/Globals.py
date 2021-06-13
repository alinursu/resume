import discord
from discord.ext import commands


GUILD_ID = 824556584834564116 # Id-ul server-ului
TOKEN = "DISCORD-BOT-TOKEN"

COMMAND_PREFIX = "!"
BOT = commands.Bot(command_prefix=COMMAND_PREFIX, intents=discord.Intents().all())
BOT_ID = 835794478619033610 # Id-ul bot-ului

BOT_ANNOUNCES_CHANNEL_NAME = "anunturi-bot" # Numele canalului in care bot-ul va trimite mesaje
DM_MESSAGES_CHANNEL_NAME = "mesaje-primite" # Numele canalului in care bot-ul va trimite mesajele primite in privat
BOT_CATEGORY_NAME = "BOT" # Numele categoriei in care se afla toate canalele bot-ului

DM_MESSAGES_QUEUE = None # Queue pentru mesajele primite in privat

STAFF_CATEGORY_NAME = "STAFF" # Numele categoriei care contine canalele disponibile doar pentru staff

MESSAGES_QUEUE = None # Queue pentru mesaje

MEMBERS_JOIN_QUEUE = None # Queue pentru membrii care intra pe server
MEMBER_JOIN_ROLE_NAME = "Nou-venit" # Numele rolului pe care il vor primi toti membrii care intra pe server
MEMBER_JOIN_CATEGORY_NAME = "Nou-Veniti" # Numele categoriei la care vor avea acces noii-veniti
MEMBER_JOIN_CHANNEL_NAME = "nou-veniti" # Numele canalului text la care vor avea acces noii-veniti

MEMBER_JOIN_CHANNEL_REACTIONS_QUEUE = None # Queue pentru reactiile la mesajul cu reguli, de pe canalul MEMBER_JOIN_CHANNEL_NAME
MEMBER_ROLE_NAME = "Elev"

SCORE_JSON_FILE_NAME = "punctaje.json" # Numele fisierului JSON in care va fi retinut punctajul fiecarui membru
SCORE_CHANNEL_NAME = "topul-punctajelor" # Canalul in care va fi afisat topul punctajelor
COMMANDS_QUEUE = None # Queue pentru comenzi

RULES_MESSAGE = """**Regulile serverului**
:one: Folositi o exprimare adecvata. Fara limbaj licentios, continut nepotrivit si alte lucruri care nu isi au locul intr-un mediu academic.
:two: Respectati ceilalti utilizatori. Abordati discutiile in mod prietenesc. Fara atacuri la persoana sau insulte.
:three: Pastrati topicul stabilit al canalelor. Evitati discutiile ce deviaza de la subiectul acestora.
:four: Nu spamati. Acordati destul timp pentru raspunsuri la intrebarile dumneavoastra, si repetati-le doar daca este neaparata nevoie.
:five: Nu este nevoie sa "intrebati ca sa intrebati". Puneti intrebarile direct.
:six: Nu perturbati buna desfasurare a sedintelor de pregatire. 
:seven: Intrebarile sau neclaritatile legate de modul de moderare al serverului se vor discuta in privat cu o persoana din echipa de moderare.
:eight: Daca observati o incalcare a regulilor, nu e nevoie sa interveniti. Semnalati evenimentul echipei de moderare printr-un tag @Moderator.

Nerespectarea regulamentului atrage aplicarea urmatoarelor sanctiuni, in functie de severitate:
- avertismente
- stergerea mesajelor problematice
- mute temporar
- ban temporar sau permanent

Va rugam sa completati acest formular de protectie a datelor personale, intrucat sedintele pot fi inregistrate pentru arhiva ASII in scop educational.
(https://forms.gle/aggXjkWwymW8U6Bv8)

In continuare, va rugam sa specificati daca sunteti de acord cu acest regulament (:thumbsup:) sau nu (:thumbsdown:).""" # Mesajul cu reguli
WARNING_FILE_NAME = "avertismente.json" # Numele fisierului JSON in care vor fi retinute numarul de avertismente al fiecarui membru