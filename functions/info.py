from traceback import format_exc

import anitopy

from libs.kitsu import RawAnimeInfo
from libs.logger import LOGS


class AnimeInfo:
    def __init__(self, name):
        self.kitsu = RawAnimeInfo()
        self.CAPTION = """
**〄 {}**

**╭────────────────────╮**
‣ **Type:** {}
‣ **Status:** {}
‣ **Episode:** {}
‣ **Audio:** Japanese
‣ **Subtitle:** English
**╰────────────────────╯**

Uploaded by ~ [𝗔𝗡𝗜𝗗𝗜𝗩𝗘™](http://t.me/ANIDIVE)
"""
        self.proper_name = self.get_proper_name_for_func(name)
        self.name = name
        self.data = anitopy.parse(name)

    async def get_english(self):
        anime_name = self.data.get("anime_title")
        try:
            anime = (await self.kitsu.search(self.proper_name)) or {}
            return anime.get("english_title") or anime_name
        except BaseException:
            LOGS.error(str(format_exc()))
            return anime_name.strip()

    async def get_poster(self):
        try:
            if self.proper_name:
                anime_poster = await self.kitsu.search(self.proper_name)
                return anime_poster.get("poster_img") or None
        except BaseException:
            LOGS.error(str(format_exc()))

    async def get_cover(self):
        try:
            if self.proper_name:
                anime_poster = await self.kitsu.search(self.proper_name)
                if anime_poster.get("anilist_id"):
                    return anime_poster.get("anilist_poster")
                return None
        except BaseException:
            LOGS.error(str(format_exc()))

    async def get_caption(self):
        try:
            if self.proper_name or self.data:
                anime = (await self.kitsu.search(self.proper_name)) or {}
                if self.data.get("episode_number") == anime.get("total_eps"):
                    anime_status = "COMPLETED"
                elif not anime.get("total_eps"):
                    anime_status = "RELEASING"
                else:
                    anime_status = "RELEASING"
                return self.CAPTION.format(
                    (await self.get_english()),
                    anime.get("type"),
                    anime_status,
                    (
                        str(self.data.get("episode_number")).zfill(2)
                        if self.data.get("episode_number")
                        else "N/A"
                    ),
                )
        except BaseException:
            LOGS.error(str(format_exc()))
            return ""

    async def rename(self, original=False):
        try:
            anime_name = self.data.get("anime_title")
            if anime_name and self.data.get("episode_number"):
                if anime_name in ["One Piece", "Detective Conan", "Chiikawa"]:
                    return (
                        f"E{self.data.get('episode_number') or ''} {(await self.get_english())} [{self.data.get('video_resolution').replace('p', 'px264' if original else 'px265') or ''}].mkv".replace(
                            "‘", ""
                        )
                        .replace("’", "")
                        .strip()
                    )
                return (
                    f"S{self.data.get('anime_season') or 1}E{self.data.get('episode_number') or ''} {(await self.get_english())} [{self.data.get('video_resolution').replace('p', 'px264' if original else 'px265') or ''}].mkv".replace(
                        "‘", ""
                    )
                    .replace("’", "")
                    .strip()
                )
            if anime_name:
                return (
                    f"{(await self.get_english())} [{self.data.get('video_resolution').replace('p', 'px264' if original else 'px265') or ''}].mkv".replace(
                        "‘", ""
                    )
                    .replace("’", "")
                    .strip()
                )
            return self.name
        except Exception as error:
            LOGS.error(str(error))
            LOGS.exception(format_exc())
            return self.name

    def get_proper_name_for_func(self, name):
        try:
            data = anitopy.parse(name)
            anime_name = data.get("anime_title")
            if anime_name and data.get("episode_number"):
                return (
                    f"{anime_name} S{data.get('anime_season')} {data.get('episode_title')}"
                    if data.get("anime_season") and data.get("episode_title")
                    else (
                        f"{anime_name} S{data.get('anime_season')}"
                        if data.get("anime_season")
                        else anime_name
                    )
                )
            return anime_name
        except Exception as error:
            LOGS.error(str(error))
            LOGS.exception(format_exc())
