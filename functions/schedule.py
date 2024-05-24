import json
import os
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from functions.config import Var
from functions.info import AnimeInfo
from functions.tools import Tools
from libs.logger import LOGS, TelegramClient


class ScheduleTasks:
    def __init__(self, bot: TelegramClient):
        self.tools = Tools()
        self.bot = bot
        if Var.SEND_SCHEDULE:
            self.sch = AsyncIOScheduler(timezone="Asia/Kolkata")
            self.sch.add_job(self.anime_timing, "cron", hour=0, minute=20)
            self.sch.start()

    async def anime_timing(self):
        try:
            _res = await self.tools.async_searcher(
                "https://subsplease.org/api/?f=schedule&h=true&tz=Asia/Kolkata"
            )
            xx = json.loads(_res)
            xxx = xx["schedule"]
            text = "<b>📆 Today's Anime Releases Schedule [IST]</b>\n\n"
            for i in xxx:
                info = AnimeInfo(i["title"])
                text += f'<a href="https://subsplease.org/shows/{i["page"]}">{(await info.get_english())}</a>\n<b>    • Time:</b> {i["time"]} hrs\n\n'
            mssg = await self.bot.send_message(
                Var.MAIN_CHANNEL, text, parse_mode="html"
            )
            await mssg.pin(notify=True)
        except Exception as error:
            LOGS.error(str(error))

    def restart(self):
        try:
            os.execl(sys.executable, sys.executable, "bot.py")
        except Exception as error:
            LOGS.error(str(error))
            self.send_message(
                Var.OWNER, f"Failed to restart: {error}"
            )
        else:
            self.send_message(
                Var.OWNER, "Bot restarted successfully!"
            )
