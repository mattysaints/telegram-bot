from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from tgbot.application.onboarding.use_cases import build_start_screen, menu_action_message
from tgbot.infrastructure.onboarding.django_user_gateway import DjangoOnboardingUserGateway
from tgbot.handlers.onboarding.manage_data import START_MENU_ACTION_PREFIX
from tgbot.presentation.telegram.onboarding_presenter import render_start_menu


user_gateway = DjangoOnboardingUserGateway()


def command_start(update: Update, context: CallbackContext) -> None:
    screen = build_start_screen(user_gateway=user_gateway, update=update, context=context)
    update.message.reply_text(text=screen.text, reply_markup=render_start_menu(screen), parse_mode=ParseMode.HTML)


def start_menu_action(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query is None or query.data is None:
        return

    action_key = query.data.replace(START_MENU_ACTION_PREFIX, '', 1)
    query.answer()
    query.message.reply_text(menu_action_message(action_key))
