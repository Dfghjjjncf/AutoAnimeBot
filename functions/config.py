from decouple import config


class Var:
    # Telegram Credentials

    API_ID = config("API_ID", default=6, cast=int)
    API_HASH = config("API_HASH", default="eb06d4abfb49dc3eeb1aeb98ae0f581e")
    BOT_TOKEN = config("BOT_TOKEN", default=None)
    SESSION = config("SESSION", default=None)

    # Database Credentials

    FIREBASE_URL = config("FIREBASE_URL", default=None)
    FIREBASE_SERVICE_ACCOUNT_FILE = config(
        "FIREBASE_SERVICE_ACCOUNT_FILE", default=None
    )

    # Channels Ids

    BACKUP_CHANNEL = config("BACKUP_CHANNEL", default=0, cast=int)
    MAIN_CHANNEL = config("MAIN_CHANNEL", cast=int)
    LOG_CHANNEL = config("LOG_CHANNEL", cast=int)
    CLOUD_CHANNEL = config("CLOUD_CHANNEL", cast=int)
    OWNER = config("OWNER", default=0, cast=int)

    # Other Configs

    THUMB = "https://telegra.ph/file/c96889c963398127b4b33.jpg"
    FFMPEG = config("FFMPEG", default="ffmpeg")
    CRF = config("CRF", default="27")
    SEND_SCHEDULE = True
