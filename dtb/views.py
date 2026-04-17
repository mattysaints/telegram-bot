import asyncio
import json
import logging
from django.views import View
from django.http import JsonResponse
from telegram import Update

from dtb.celery import app
from dtb.settings import DEBUG, TELEGRAM_TOKEN
from tgbot.dispatcher import build_application

logger = logging.getLogger(__name__)

# Build the Application once at module level (holds bot + handlers)
_application = build_application(TELEGRAM_TOKEN)


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, _application.bot)
    asyncio.run(_application.process_update(update))


def index(request):
    return JsonResponse({"error": "sup hacker"})


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        if DEBUG:
            process_telegram_event(json.loads(request.body))
        else:
            # Process Telegram event in Celery worker (async)
            # Don't forget to run it and & Redis (message broker for Celery)!
            # Locally, You can run all of these services via docker-compose.yml
            process_telegram_event.delay(json.loads(request.body))

        # e.g. remove buttons, typing event
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request received! But nothing done"})
