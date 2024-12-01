from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    Updater,
)

from .common.db_querrys import (
    get_schedule
)


def schedule(update: Update, context: CallbackContext):
    current_meetup = context.user_data["current_meetup"]
    schedule = get_schedule(current_meetup)
    buttons = [
            [
                InlineKeyboardButton(
                    "В меню",
                    callback_data="menu",
                )
            ]
    ]
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        schedule,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        CallbackQueryHandler(schedule, pattern="^schedule$")
    )
    return updater.dispatcher
