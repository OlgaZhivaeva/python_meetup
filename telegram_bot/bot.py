import logging

from django.conf import settings
from telegram.ext import Updater

from .start import handlers_register as start
from .speech_speaker import handlers_register as speaker


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(settings.TG_BOT_TOKEN, use_context=True)
    updater.dispatcher = start(updater)
    updater.dispatcher = speaker(updater)
    updater.start_polling()
    updater.idle()
