import asyncio
import logging

from telethon import Button, TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError

from functions.config import Var

logging.basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] : %(message)s",
    handlers=[
        logging.FileHandler("AutoAnimeBot.log", mode="w", encoding="utf-8"),
        logging.StreamHandler(),
    ],
    level=logging.INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
)
LOGS = logging.getLogger("AutoAnimeBot")
TelethonLogger = logging.getLogger("Telethon")
TelethonLogger.setLevel(logging.INFO)

LOGS.info(
    """
                        Auto Anime Bot

    """
)


class Reporter:
    def __init__(self, client: TelegramClient, file_name: str):
        self.client: TelegramClient = client
        self.file_name = file_name
        self.msg = None

    async def alert_new_file_founded(self):
        await self.awake()
        msg = await self.client.send_message(
            Var.LOG_CHANNEL,
            f"**➤ Anime Name:** {self.file_name}\n\n__Downloading files...__",
        )
        self.msg = msg

    async def started_compressing(self, btn):
        self.msg = await self.msg.edit(
            f"**➤ Anime Name:** {self.file_name}\n\n__Encoding files...__",
            buttons=btn,
        )

    async def started_renaming(self):
        self.msg = await self.msg.edit(
            f"**➤ Anime Name:** {self.file_name}\n\n__Renaming file...__",
            buttons=[[Button.inline("✒️", data="uwu")]],
        )

    async def started_uploading(self):
        self.msg = await self.msg.edit(
            f"**➤ Anime Name:** {self.file_name}\n\n__Uploading file...__",
            buttons=[],
        )

    async def all_done(self):
        self.msg = await self.msg.edit(
            f"**➤ Anime Name:** {self.file_name}\n\n**__Task Completed!__**"
        )

    async def awake(self):  # in case
        if not self.client.is_connected():
            await self.client.connect()

    async def report_error(self, msg, log=False):
        txt = f"[ERROR] {msg}"
        if log:
            LOGS.error(txt[0])
        try:
            await self.client.send_message(Var.LOG_CHANNEL, f"{txt[:4096]}")
        except FloodWaitError as fwerr:
            await self.client.disconnect()
            LOGS.info("Sleeping Becoz Of Floodwait...")
            await asyncio.sleep(fwerr.seconds + 10)
            await self.client.connect()
        except ConnectionError:
            await self.client.connect()
        except Exception as err:
            LOGS.error(str(err))
