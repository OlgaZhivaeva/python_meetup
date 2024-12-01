from datetime import datetime

from telegram import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    error,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    Filters,
    MessageHandler,
    Updater,
)

from .common.extra_funcs import safe_send_message


def speech_begin_check(update: Update, context: CallbackContext):
    if not context.bot_data.get("current_speaker"):
        begin_speech(update, context)
    else:
        buttons = [
            [InlineKeyboardButton("Прервать", callback_data="begin_speech")],
            [InlineKeyboardButton("Отмена", callback_data="start")],
        ]
        message = f"""В данный момент идет выступление "{context.bot_data["current_topic"].topic}"
Уверены, что хотите прервать выступление?"""
        safe_send_message(update, message, buttons)


def begin_speech(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if context.bot_data.get("current_speaker"):
        context.bot.send_message(
            text="Выступление завершено",
            chat_id=context.bot_data["current_speaker_chat_id"],
            reply_markup=ReplyKeyboardRemove(),
        )

    speaker_chat_id = update.effective_chat.id
    speech_topic = context.user_data["planning_speech"].topic
    context.bot_data["current_topic"] = context.user_data["planning_speech"]
    context.bot_data["current_speaker"] = context.user_data["participant"]
    context.bot_data["current_speaker_chat_id"] = speaker_chat_id

    current_time = datetime.now().strftime("%H:%M")
    speech_time_limit = context.user_data["planning_speech"].time_limit
    message_topic = f"""Доклад "{speech_topic}"
Во время выступления вопросы участников будут приходить в этот чат.
Для завершения выступления нажмите кнопку снизу."""
    message_time = f"""Начало в {current_time}
Вам отведено {speech_time_limit} минут
"""

    reply_keyboard = [["Завершить выступление"]]
    context.bot.send_message(
        text=message_topic,
        chat_id=speaker_chat_id,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            resize_keyboard=True,
        ),
    )
    speech_time_message_id = context.bot.send_message(
        text=message_time,
        chat_id=speaker_chat_id,
    ).message_id
    context.bot.pin_chat_message(
        chat_id=speaker_chat_id, message_id=speech_time_message_id
    )
    context.user_data["speech_time_message_id"] = speech_time_message_id

    for participant in context.user_data["current_meetup"].participants.all():
        if participant != context.user_data["participant"]:
            try:
                context.bot.send_message(
                    text=f'Выступление "{speech_topic}" началось',
                    chat_id=participant.tg_id,
                )
            except error.BadRequest:
                continue


def finish_speech(update: Update, context: CallbackContext):
    # query = update.callback_query
    # query.answer()
    chat_id = update.effective_chat.id
    context.bot.unpin_chat_message(
        chat_id=chat_id,
        message_id=context.user_data["speech_time_message_id"],
    )
    context.bot.send_message(
        text="Выступление завершено",
        chat_id=chat_id,
        reply_markup=ReplyKeyboardRemove(),
    )

    context.bot_data["current_topic"] = None
    context.bot_data["current_speaker"] = None
    context.bot_data["current_speaker_chat_id"] = None

    speech_topic = context.user_data["planning_speech"].topic
    for participant in context.user_data["current_meetup"].participants.all():
        if participant != context.user_data["participant"]:
            try:
                context.bot.send_message(
                    text=f'Выступление "{speech_topic}" закончилось',
                    chat_id=participant.tg_id,
                )
            except error.BadRequest:
                continue


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        CallbackQueryHandler(
            speech_begin_check, pattern="^speech_begin_check$"
        )
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(begin_speech, pattern="^begin_speech$")
    )
    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(r"^Завершить выступление$"), finish_speech
        )
    )
    return updater.dispatcher
