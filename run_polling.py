import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dtb.settings')
django.setup()

from dtb.settings import TELEGRAM_TOKEN
from tgbot.dispatcher import build_application
from tgbot.system_commands import set_up_commands


def run_polling(tg_token: str = TELEGRAM_TOKEN):
    """ Run bot in polling mode """
    app = build_application(tg_token)

    # Set up bot commands
    async def post_init(application):
        try:
            await set_up_commands(application.bot)
        except Exception:
            import logging
            logging.getLogger(__name__).exception("Failed to set Telegram commands on startup")

    app.post_init = post_init

    print("Polling has started")
    app.run_polling()


if __name__ == "__main__":
    run_polling()
