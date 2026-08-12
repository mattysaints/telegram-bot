from datetime import timedelta

from django.utils.timezone import now
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from tgbot.handlers.admin import static_text
from tgbot.handlers.admin.utils import _get_csv_from_qs_values
from tgbot.handlers.utils.decorators import admin_only, send_typing_action
from users.models import User


@admin_only
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Show help info about all secret admins commands """
    await update.message.reply_text(static_text.secret_admin_commands)


@admin_only
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Show help info about all secret admins commands """
    text = static_text.users_amount_stat.format(
        user_count=User.objects.count(),  # count may be ineffective if there are a lot of users.
        active_24=User.objects.filter(updated_at__gte=now() - timedelta(hours=24)).count()
    )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


@admin_only
@send_typing_action
async def export_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # in values argument you can specify which fields should be returned in output csv
    users = User.objects.all().values()
    csv_users = _get_csv_from_qs_values(users)
    await update.message.reply_document(csv_users)
