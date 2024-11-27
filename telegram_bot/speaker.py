from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    Updater,
)

from .db_querrys import querries


def speaker_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    buttons = [
        [
            InlineKeyboardButton(
                "Начать выступление", callback_data="begin_speech"
            )
        ],
        [
            InlineKeyboardButton(
                "Закончить выступление", callback_data="finish_speech"
            )
        ],
        [
            InlineKeyboardButton(
                "Показать вопросы", callback_data="show_questions"
            )
        ],
    ]
    context.bot.send_message(
        text=next_message,
        chat_id=chat_id,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def begin_speech(update: Update, context: CallbackContext):
    pass


def finish_speech(update: Update, context: CallbackContext):
    pass


def show_questions(update: Update, context: CallbackContext):
    pass


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        CallbackQueryHandler(
            speaker_menu, pattern="^speaker_menu$"
        )
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(begin_speech, pattern="^begin_speech$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(finish_speech, pattern="^finish_speech$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(show_questions, pattern="^show_questions$")
    )
    return updater.dispatcher
