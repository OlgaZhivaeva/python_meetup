from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from .start import menu


def speech_questions(update: Update, context: CallbackContext):
    current_topic = context.bot_data.get("current_topic")
    current_speaker = context.bot_data.get("current_speaker")
    buttons = [
            [
                InlineKeyboardButton(
                    "В меню",
                    callback_data="to_menu",
                )
            ]
    ]
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "".join([
            f'Сейчас выступает {current_speaker}\n',
            f'Тема выступления {current_topic}\n\n',
            'Задать вопрос Вы можете в чате.\n\n',
            'Для выхода из режима задачи вопросов нажмите на кнопку "В меню"\n'
        ]),
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return "QUESTION"


def send_question(update: Update, context: CallbackContext):
    question = update.message.text
    context.bot.send_message(
            text=question,
            chat_id=context.bot_data["current_speaker_chat_id"],
        )
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="Вопрос передан докладчику"
        )


def to_menu(update: Update, context: CallbackContext):
    menu(update, context)
    return ConversationHandler.END


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    speech_questions, pattern="^speech_questions$"
                )
            ],
            states={
                "QUESTION": [
                    MessageHandler(
                        Filters.text & ~Filters.command, send_question
                    ),
                ]
            },
            fallbacks=[CallbackQueryHandler(to_menu, pattern="^to_menu$")],
        )
    )
    return updater.dispatcher
