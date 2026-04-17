from functools import wraps
from typing import Callable

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from users.models import User


def admin_only(func: Callable):
    """
    Admin only decorator
    Used for handlers that only admins have access to
    """

    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = User.get_user(update, context)

        if not user.is_admin:
            return

        return await func(update, context, *args, **kwargs)

    return wrapper


def send_typing_action(func: Callable):
    """Sends typing action while processing func command."""

    @wraps(func)
    async def command_func(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        await update.effective_chat.send_action(ChatAction.TYPING)
        return await func(update, context, *args, **kwargs)

    return command_func
