import asyncio
import logging
import os
import sys
import time

import aiohttp
import httpx
import spamwatch
from Obito_Probot.utils import Sylviorus
import telegram.ext as tg
from aiohttp import ClientSession
from motor import motor_asyncio
from odmantic import AIOEngine
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, PeerIdInvalid
from Python_ARQ import ARQ
from redis import StrictRedis
from telegram import Chat
from telethon import TelegramClient
from telethon.sessions import StringSession
from Obito_Probot.config import Development as Config

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = Config.TOKEN

    try:
        OWNER_ID = Config.OWNER_ID
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = "Namikaze_2op"

    try:
        REDLIONS = Config.REDLIONS
        DEV_USERS = config.DEV_USERS
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
          SPRYZONS = Config.SPRYZONS
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        LUINORS = Config.LUINORS
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        FAFNIRS = Config.FAFNIRS
    except ValueError:
        raise Exception("Your fafnir users list does not contain valid integers.")

    INFOPIC = True
    EVENT_LOGS = -1001501815938
    ERROR_LOGS = -1001501815938  # Error Logs (Channel Ya Group Choice Is Yours) (-100)

    WEBHOOK = False
    URL =   "https://.herokuapp.com" # Does not contain token
    PORT = 500
    CERT_PATH = None
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ARQ_API_URL = "https://thearq.tech"  # Don't Change
    ARQ_API_KEY = "RDERJR-UMUNTF-PGKWKS-DYPWDF-ARQ"
    REM_BG_API_KEY = None # From:- https://www.remove.bg/
    BOT_ID = 5127077268
    BOT_USERNAME = "Obito_Probot"
    BOT_NAME = "Obito Uchiha 『VƗŁŁȺƗNS』" # Name Of your Bot.4

    REDIS_URL = ""
    HEROKU_API_KEY = ""
    HEROKU_APP_NAME = ""
    TEMP_DOWNLOAD_DIRECTORY = "./"
    OPENWEATHERMAP_ID = "d5775e35b90f4029b3665d8e0dfa3c94"
    DEL_CMDS = True
    STRICT_GBAN = True
    STRICT_GMUTE = True
    WORKERS = 8
    BAN_STICKER = "CAADAgADOwADPPEcAXkko5EB3YGYAg"
    ALLOW_EXCL = True
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY =  Config.TIME_API_KEY
    AI_API_KEY = None
    WALL_API = None
    SUPPORT_CHAT = "Villainevil_Support"
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    STRING_SESSION = "BQCvHTBohT8Ir1bvVkSBbi_8DuCr3Iyh-IwsRmW5I7Od03oWdtq9XMYIMuGPbZQ2mqz0aIrHKe3AHDw_Vk7-ZkQ6R612qx7IOUvI-aXXtT4ooRxGPN_ttG_kXgkDmEdKkljjQVybt011Be2-4_jpXyKp3tdTjbD6vpyKHlrTgk7_cWRYYcxfNUJXSsaQUTBaLmsP1UQBc04NHChFA1SWhRT7O0ilSK2RaDUIVF0SsrAsXEoH1MMSkyA0pAEXjPWal2w2aICRYgwEmfSUmlMPTsDoVWTkD9JuxMLoe4xCkGjieA6KRidPIdMTKTiR5B8moUL1RMGZsIKrUXRZFtgHDDjcAAAAAHMBahwA"

    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    HELP_IMG = os.environ.get("HELP_IMG", True)
    GROUP_START_IMG = "https://telegra.ph/file/5bb0ab9d4e258de4f8e6c.mp4"
    OBITO_PHOTO = "https://telegra.ph/file/7b8da175b674f6e05f30f.jpg"

    try:
        BL_CHATS = {int(x) for x in os.environ.get("BL_CHATS", "").split()}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

else:

    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        REDLIONS = {int(x) for x in Config.REDLIONS or []}
        DEV_USERS = {int(x) for x in Config.DEV_USERS or []}
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        SPRYZONS = {int(x) for x in Config.SPRYZONS or []}
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        LUINORS = {int(x) for x in Config.LUINORS or []}
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        FAFNIRS = {int(x) for x in Config.FAFNIRS or []}
    except ValueError:
        raise Exception("Your fafnir users list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ARQ_API_URL = Config.ARQ_API_URL
    ARQ_API_KEY = Config.ARQ_API_KEY

    BOT_USERNAME = Config.BOT_USERNAME
    BOT_NAME = Config.BOT_NAME

    DB_URL = Config.SQLALCHEMY_DATABASE_URL
    REDIS_URL = Config.REDIS_URL
    HEROKU_API_KEY = Config.HEROKU_API_KEY
    HEROKU_APP_NAME = Config.HEROKU_APP_NAME
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    BOT_ID = Config.BOT_ID
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    STRICT_GMUTE = Config.STRICT_GMUTE
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    AI_API_KEY = Config.AI_API_KEY
    WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    INFOPIC = Config.INFOPIC
    STRING_SESSION = Config.STRING_SESSION
    HELP_IMG = Config.HELP_IMG
    START_IMG = Config.START_IMG
    OBITO_PHOTO = Config.OBITO_PHOTO

    try:
        BL_CHATS = {int(x) for x in Config.BL_CHATS or []}
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")


REDLIONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(1791795037)
DEV_USERS.add(5239506592)

REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)

try:

    REDIS.ping()

    LOGGER.info("[obito]: Connecting To obito • Data Center • Mumbai • Redis Database")

except BaseException:

    raise Exception(
        "[obito ERROR]: Your obito • Data Center • Mumbai • Redis Database Is Not Alive, Please Check Again."
    )

finally:

    REDIS.ping()

    LOGGER.info(
        "[obito]: Connection To The obito • Data Center • Mumbai • Redis Database Established Successfully!"
    )

SYL = Sylviorus()

if not SPAMWATCH_API:
    sw = None
    LOGGER.warning("SpamWatch API key missing! recheck your config.")
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except:
        sw = None
        LOGGER.warning("Can't connect to SpamWatch!")

ubot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
try:
    ubot.start()
except BaseException:
    print("Userbot Error ! Have you added a STRING_SESSION in deploying??")
    sys.exit(1)

updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient("Obito", API_ID, API_HASH)
pbot = Client("Obitopbot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
dispatcher = updater.dispatcher

print("[VILLAINS]: Connecting To Obito • Data Center • Mumbai • MongoDB Database")
mongodb = MongoClient(MONGO_DB_URL, MONGO_PORT)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
db = motor[MONGO_DB]
engine = AIOEngine(motor, MONGO_DB)
print("[INFO]: INITIALZING AIOHTTP SESSION")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

ubot2 = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
try:
    ubot2.start()
except BaseException:
    print("Userbot Error ! Have you added a STRING_SESSION in deploying??")
    sys.exit(1)

REDLIONS = list(REDLIONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
LUINORS = list(LUINORS)
SPRYZONS = list(SPRYZONS)
FAFNIRS = list(FAFNIRS)

# Load at end to ensure all prev variables have been set
from Obito_Probot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
