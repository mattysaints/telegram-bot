from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.domain.onboarding import StartScreen
from tgbot.handlers.onboarding.manage_data import START_MENU_ACTION_PREFIX


def render_start_menu(screen: StartScreen) -> InlineKeyboardMarkup:
    rows = []
    for action in screen.actions:
        button = InlineKeyboardButton(
            text=action.label,
            url=action.url,
            callback_data=None if action.url else f"{START_MENU_ACTION_PREFIX}{action.key}",
        )
        rows.append([button])

    return InlineKeyboardMarkup(rows)

