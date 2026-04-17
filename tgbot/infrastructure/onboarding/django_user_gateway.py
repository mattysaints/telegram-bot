from telegram import Update
from telegram.ext import ContextTypes

from tgbot.domain.onboarding import UserSnapshot
from users.models import User


class DjangoOnboardingUserGateway:
    def get_user_snapshot(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> UserSnapshot:
        user, created = User.get_user_and_created(update, context)
        return UserSnapshot(user_id=user.user_id, first_name=user.first_name, is_new=created)
