from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.domain.onboarding import StartScreen
from tgbot.handlers.onboarding.manage_data import START_MENU_ACTION_PREFIX


def render_start_menu(screen: StartScreen) -> InlineKeyboardMarkup:
    rows = []
    pair = []
    for action in screen.actions:
        pair.append(
            InlineKeyboardButton(
                text=action.label,
                callback_data=f"{START_MENU_ACTION_PREFIX}{action.key}",
            )
        )
        if len(pair) == 2:
            rows.append(pair)
            pair = []

    if pair:
        rows.append(pair)

    return InlineKeyboardMarkup(rows)

