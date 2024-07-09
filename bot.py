import re
from traceback import format_exc

from telethon import Button, events

from core.bot import Bot
from core.executors import Executors
from database import DataBase
from functions.info import AnimeInfo
from functions.schedule import ScheduleTasks, Var
from functions.tools import Tools, asyncio
from functions.utils import AdminUtils
from libs.ariawarp import Torrent
from libs.logger import LOGS, Reporter
from libs.subsplease import SubsPlease

tools = Tools()
tools.init_dir()
bot = Bot()
dB = DataBase()
subsplease = SubsPlease(dB)
torrent = Torrent()
schedule = ScheduleTasks(bot)
admin = AdminUtils(dB, bot)


@bot.on(
    events.NewMessage(
        incoming=True, pattern="^/start ?(.*)", func=lambda e: e.is_private
    )
)
async def _start(event):
    xnx = await event.reply("**Connecting...**")
    msg_id = event.pattern_match.group(1)
    dB.add_broadcast_user(event.sender_id)
    if msg_id:
        if msg_id.isdigit():
            msg = await bot.get_messages(Var.BACKUP_CHANNEL, ids=int(msg_id))
            await event.reply(msg)
            await event.delete()
        else:
            await xnx.delete()
    else:
        if event.sender_id == Var.OWNER:
            return await xnx.edit(
                "**Bot Admin Settings**",
                buttons=admin.admin_panel(),
            )
        await event.reply(
            file="https://graph.org/file/8bb750efbe7f08176e2ae.png",
            message=f"**Hey {event.sender.first_name}!,\n\n   I am Auto Animes Store & Automater Encoder Build with ❤️ !!**",
            buttons=[
                [
                    Button.url("📣 Updates", url="t.me/ANIDIVE"),
                    Button.url(
                        "🗂️ Anime Index",
                        url="https://t.me/Anime_Index0",
                    ),
                ]
            ],
        )
    await xnx.delete()


@bot.on(events.callbackquery.CallbackQuery(data=re.compile("tas_(.*)")))
async def _(e):
    await tools.stats(e)


@bot.on(events.callbackquery.CallbackQuery(data="slog"))
async def _(e):
    await admin._logs(e)


@bot.on(events.callbackquery.CallbackQuery(data="sret"))
async def _(e):
    await admin._restart(e, schedule)


@bot.on(events.callbackquery.CallbackQuery(data="entg"))
async def _(e):
    await admin._encode_t(e)


@bot.on(events.callbackquery.CallbackQuery(data="butg"))
async def _(e):
    await admin._btn_t(e)


@bot.on(events.callbackquery.CallbackQuery(data="scul"))
async def _(e):
    await admin._sep_c_t(e)


@bot.on(events.callbackquery.CallbackQuery(data="cast"))
async def _(e):
    await admin.broadcast_bt(e)


@bot.on(events.callbackquery.CallbackQuery(data="bek"))
async def _(e):
    await e.edit(buttons=admin.admin_panel())


async def anime(data):
    try:
        torr = [data.get("480p"), data.get("720p"), data.get("1080p")]
        anime_info = AnimeInfo(torr[0].title)
        poster = await tools._poster(bot, anime_info)
        if dB.is_separate_channel_upload():
            chat_info = await tools.get_chat_info(bot, anime_info, dB)
            await poster.edit(
                buttons=[
                    [
                        Button.url(
                            f"✨ EPISODE {anime_info.data.get('episode_number', '')}".strip(),
                            url=chat_info["invite_link"],
                        )
                    ]
                ]
            )
            poster = await tools._poster(bot, anime_info, chat_info["chat_id"])
        btn = [[]]
        original_upload = dB.is_original_upload()
        button_upload = dB.is_button_upload()
        for i in torr:
            try:
                filename = f"downloads/{i.title}"
                reporter = Reporter(bot, i.title)
                await reporter.alert_new_file_founded()
                await torrent.download_magnet(i.link, "./downloads/")
                exe = Executors(
                    bot,
                    dB,
                    {
                        "original_upload": original_upload,
                        "button_upload": button_upload,
                    },
                    filename,
                    AnimeInfo(i.title),
                    reporter,
                )
                result, _btn = await exe.execute()
                if result:
                    if _btn:
                        if len(btn[0]) == 2:
                            btn.append([_btn])
                        else:
                            btn[0].append(_btn)
                        await poster.edit(buttons=btn)
                    asyncio.ensure_future(exe.further_work())
                    continue
                await reporter.report_error(_btn, log=True)
            except BaseException:
                await reporter.report_error(str(format_exc()), log=True)
    except BaseException:
        LOGS.error(str(format_exc()))


try:
    bot.loop.run_until_complete(subsplease.on_new_anime(anime))
    bot.run()
except KeyboardInterrupt:
    subsplease._exit()
