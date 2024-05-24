from telethon import Button, events

from core.bot import Bot, Var, asyncio
from database import DataBase


class AdminUtils:
    def __init__(self, dB: DataBase, bot: Bot):
        self.db = dB
        self.bot = bot

    def admin_panel(self):
        btn = [
            [
                Button.inline("🤖 Logs", data="slog"),
                Button.inline("♻️ Restart", data="sret"),
            ],
            [
                Button.inline("✂️ Encode [Toogle]", data="entg"),
            ],
            [Button.inline("🔲 Button Upload [Toogle]", data="butg")],
            [Button.inline("🗂️ Separate Channel Upload [Toogle]", data="scul")],
            [Button.inline("📣 Broadcast", data="cast")],
        ]
        return btn

    def back_btn(self):
        return [[Button.inline("◀️ Back", data="bek")]]

    async def _logs(self, e):
        await e.reply(file="AutoAnimeBot.log")

    async def _restart(self, e, schedule):
        await e.reply("**Restarting...**")
        schedule.restart()

    async def _encode_t(self, e):
        if self.db.is_original_upload():
            self.db.toggle_original_upload()
            return await e.edit("**File Compression - ON**", buttons=self.back_btn())
        self.db.toggle_original_upload()
        return await e.edit("**File Compression - OFF**", buttons=self.back_btn())

    async def _btn_t(self, e):
        if self.db.is_separate_channel_upload():
            return await e.edit(
                "You Can't `On/Off` The Button Upload When Seprate Channel Is Enabled!",
                buttons=self.back_btn(),
            )
        if self.db.is_button_upload():
            self.db.toggle_button_upload()
            return await e.edit("**Button Upload - OFF**", buttons=self.back_btn())
        self.db.toggle_button_upload()
        return await e.edit("**Button Upload - ON", buttons=self.back_btn())

    async def _sep_c_t(self, e):
        if Var.SESSION:
            if self.db.is_button_upload():
                if self.db.is_separate_channel_upload():
                    self.db.toggle_separate_channel_upload()
                    return await e.edit(
                        "**Separate Channel Upload - OFF**",
                        buttons=self.back_btn(),
                    )
                self.db.toggle_separate_channel_upload()
                return await e.edit(
                    "**Separate Channel Upload - ON**",
                    buttons=self.back_btn(),
                )
            else:
                return await e.edit(
                    "**To Use The Separate Channel Upload, First You Have To Enable Button Upload!!**",
                    buttons=self.back_btn(),
                )
        else:
            return await e.edit(
                "**To Use The Separate Channel Upload, First You Have To Add SESSION Variable in The Bot!!**",
                buttons=self.back_btn(),
            )

    async def broadcast_bt(self, e):
        users = self.db.get_broadcast_user()
        await e.edit("**Please Use This Feature Responsibly ⚠️**")
        await e.reply(
            f"**Send a single Message To Broadcast 😉**\n\n**There are** `{len(users)}` **Users Currently Using Me👉🏻**.\n\nSend /cancel to Cancel Process."
        )
        async with e.client.conversation(e.sender_id) as cv:
            reply = cv.wait_event(events.NewMessage(from_users=e.sender_id))
            repl = await reply
            await e.delete()
            if repl.text and repl.text.startswith("/cancel"):
                return await repl.reply("Broadcast Cancelled!")
        sent = await repl.reply("📣 Broadcasting Your Post...")
        done, er = 0, 0
        for user in users:
            try:
                if repl.poll:
                    await repl.forward_to(int(user))
                else:
                    await e.client.send_message(int(user), repl.message)
                await asyncio.sleep(0.2)
                done += 1
            except BaseException as ex:
                er += 1
                print(ex)
        await sent.edit(
            f"**Broadcasting Completed!**\n\n**Completed:** `{done}`\n**Errors:** `{er}`"
        )
