import datetime

from telegram import InlineKeyboardMarkup
from django.utils import timezone

# Погрешность, чтобы не считать начало / конец встречи
INACCURACY = 12


def get_datetime_now_with_inaccuracy_less():
    return get_current_datetime() - datetime.timedelta(hours=INACCURACY)


def get_datetime_now_with_inaccuracy_greater():
    return get_current_datetime() + datetime.timedelta(hours=INACCURACY)


def get_current_datetime():
    return timezone.now()


def safe_send_message(update, message, buttons=None):
    query = update.callback_query
    if query:
        query.answer()
        query.edit_message_text(
            message,
            reply_markup=buttons and InlineKeyboardMarkup(buttons) or None,
        )
    else:
        update.message.reply_text(
            message,
            reply_markup=buttons and InlineKeyboardMarkup(buttons) or None,
        )
