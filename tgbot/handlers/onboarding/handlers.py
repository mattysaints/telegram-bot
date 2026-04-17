import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from tgbot.application.onboarding.use_cases import build_start_screen, menu_action_message
from tgbot.infrastructure.onboarding.django_user_gateway import DjangoOnboardingUserGateway
from tgbot.handlers.onboarding import static_text
from tgbot.handlers.onboarding.manage_data import START_MENU_ACTION_PREFIX
from tgbot.presentation.telegram.onboarding_presenter import render_start_menu
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User


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


def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )