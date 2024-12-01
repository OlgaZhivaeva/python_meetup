import logging

from django.conf import settings
from telegram import Update, Bot
from telegram.ext import Updater, CallbackContext

from .start import handlers_register as start
from .speech_speaker import handlers_register as speaker
from .speech_questions import handlers_register as questions
from .comrad_search import handlers_register as comrad_search
from .schedule import handlers_register as schedule

from .start import start as restart


TG_BOT_TOKEN = settings.TG_BOT_TOKEN


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# Обработчик ошибок
def error(update: Update, context: CallbackContext):
    try:
        update.message.reply_text("Произошла ошибка. Возвращаемся на главную.")
        restart(update, context)
    except Exception as e:
        logger.error(f"Не получилось отловить ошибку: {e}")


def send_messages_for_all(tg_ids, message='Привет'):
    bot = Bot(token=TG_BOT_TOKEN)
    for tg_id in tg_ids:
        try:
            bot.send_message(chat_id=tg_id, text=message)
        except Exception:
            pass


def main():
    updater = Updater(TG_BOT_TOKEN, use_context=True)
    updater.dispatcher = start(updater)
    updater.dispatcher = comrad_search(updater)
    updater.dispatcher = speaker(updater)
    updater.dispatcher = schedule(updater)
    updater.dispatcher = questions(updater)
    # updater.dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()
