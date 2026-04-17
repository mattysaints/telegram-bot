"""
    Telegram event handlers
"""
import logging

from telegram.ext import (
    Application,
    filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import broadcast_command
from tgbot.handlers.onboarding.manage_data import START_MENU_PATTERN

from tgbot.handlers.utils import files, error
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.location import handlers as location_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.broadcast_message import handlers as broadcast_handlers


logger = logging.getLogger(__name__)


def setup_dispatcher(app: Application) -> Application:
    """
    Adding handlers for events from Telegram
    """
    # onboarding
    app.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    app.add_handler(CallbackQueryHandler(onboarding_handlers.start_menu_action, pattern=START_MENU_PATTERN))

    # admin commands
    app.add_handler(CommandHandler("admin", admin_handlers.admin))
    app.add_handler(CommandHandler("stats", admin_handlers.stats))
    app.add_handler(CommandHandler('export_users', admin_handlers.export_users))

    # location
    app.add_handler(CommandHandler("ask_location", location_handlers.ask_for_location))
    app.add_handler(MessageHandler(filters.LOCATION, location_handlers.location_handler))

    # broadcast message
    app.add_handler(
        MessageHandler(filters.Regex(rf'^{broadcast_command}(/s)?.*'), broadcast_handlers.broadcast_command_with_message)
    )
    app.add_handler(
        CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
    )

    # files
    app.add_handler(MessageHandler(
        filters.ANIMATION, files.show_file_id,
    ))

    # handling errors
    app.add_error_handler(error.send_stacktrace_to_tg_chat)

    return app


def build_application(tg_token: str) -> Application:
    app = Application.builder().token(tg_token).build()
    setup_dispatcher(app)
    return app
