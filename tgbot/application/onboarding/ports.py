from typing import Protocol

from telegram import Update
from telegram.ext import CallbackContext

from tgbot.domain.onboarding import UserSnapshot


class OnboardingUserGateway(Protocol):
	def get_user_snapshot(self, update: Update, context: CallbackContext) -> UserSnapshot:
		...

