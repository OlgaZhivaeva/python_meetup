import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from .common.db_querrys import (
    check_questionnaire,
    check_questionnaires,
    get_unseen_questionnaire,
    update_questionnaire
)
from .start import menu


# Уведомляем при отсутствии анкеты (первый запуск на митапе)
def inform_questionnaire(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    buttons = [
            [InlineKeyboardButton(
                "Назад",
                callback_data="menu",
            )],
            [InlineKeyboardButton(
                "Заполнить анкету",
                callback_data="request_full_name",
            )]
        ]
    query.edit_message_text(
        "".join([
            'Раздел "Знакомства" позволяет посмотреть анкеты других участников конференции для дальнейшей связи с ними в телеграмм.\n\n',
            'Для просмотра анкет необходимо сформировать заполнить свою анкету, указав следующие даннные:\n\n',
            'Ваше ФИО\n',
            'Стэк\n',
            'О себе (кратко)\n',
            'Если Вы хотите продолжить - нажмите "Заполнить анкету"\n'
            ]),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# ==================== START CONVERSATION ====================

def request_full_name(update: Update, context: CallbackContext):
    query = update.callback_query
    buttons = [
        [
            InlineKeyboardButton(
                "Пропустить", callback_data="skip_full_name"
            )
        ]
    ]
    query.answer()
    context.user_data['last_message'] = query.edit_message_text(
        text="Напишите Ваше ФИО",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return "FULL_NAME"


def get_full_name(update: Update, context: CallbackContext):
    full_name = (
        update.message.text if update.message else ""
    )
    context.user_data["full_name"] = full_name
    if update.message:
        update.message.delete()
    request_stack(update, context)
    return "STACK"


def request_stack(update: Update, context: CallbackContext):
    context.user_data['last_message'].edit_text(
        "Напишите списком ваш стэк"
    )


def get_stack(update: Update, context: CallbackContext):
    stack = (
        update.message.text
    )
    context.user_data['stack'] = stack
    update.message.delete()
    request_bio(update, context)
    return "BIO"


def request_bio(update: Update, context: CallbackContext):
    context.user_data['last_message'].edit_text(
        "Напишите о себе"
    )


def get_bio(update: Update, context: CallbackContext):
    bio = (
        update.message.text if update.message else ""
    )
    context.user_data['bio'] = bio
    update.message.delete()
    end_questionnaire(update, context)
    return ConversationHandler.END


def end_questionnaire(update: Update, context: CallbackContext):
    bio = context.user_data['bio']
    stack = context.user_data['stack']
    full_name = context.user_data['full_name']
    meetup = context.user_data['current_meetup']
    participant = context.user_data['participant']
    update_questionnaire(meetup, participant, full_name, stack, bio)
    chat_id = update.effective_chat.id
    success_message = context.bot.send_message(
        chat_id=chat_id,
        text="Анкета успешно создана. Переходим к списку анкет."
    )
    show_questionnaires(update, context)
    time.sleep(2)
    success_message.delete()

# ==================== END CONVERSATION ====================


# Сброс истории просмотра анкет
def reset_history(update: Update, context: CallbackContext):
    context.user_data["last_questionnaire_id"] = None
    show_questionnaires(update, context)


# Отображаем анкеты
def show_questionnaires(update: Update, context: CallbackContext):
    current_meetup = context.user_data["current_meetup"]
    participant = context.user_data["participant"]
    # Проверяем, существуют-ли анкеты
    is_any_questionnaire = bool(
        check_questionnaires(participant.id, current_meetup.id)
    )
    if not is_any_questionnaire:
        no_questionnaires_message = (
            "К сожалению, анкеты отсутствуют.\nПожалуйста, зайдите позже."
        )
        chat_id = update.effective_chat.id
        message = context.bot.send_message(
            chat_id=chat_id,
            text=no_questionnaires_message
        )
        menu(update, context)
        time.sleep(2)
        message.delete()
        return
    # Отображаем непросмотренные анкеты и запоминаем, что просмотрели
    participant = context.user_data["participant"]
    last_questionnaire_id = context.user_data.get("last_questionnaire_id")
    questionnaire = get_unseen_questionnaire(
        participant.id,
        current_meetup.id,
        last_questionnaire_id
    )
    if not questionnaire:
        message = (
            "К сожалению, анкеты закончились.\nПожалуйста, зайдите позже и нажмите 'Далее', либо можете сбросить историю просмотра, нажав на кнопку 'Сброс истории'."
        )
    else:
        context.user_data["last_questionnaire_id"] = questionnaire.id
        message = "".join([
            f'Анкета пользователя {questionnaire.participant.tg_username}\n',
            f'Полное имя: {questionnaire.participant.full_name}\n',
            f'Стэк: {questionnaire.stack}\n',
            f'О себе: {questionnaire.bio}\n',
            ])
    buttons = [
            [
                InlineKeyboardButton(
                    "В меню",
                    callback_data="menu",
                ),
                InlineKeyboardButton(
                    "Далее",
                    callback_data="show_questionnaires",
                ),
                InlineKeyboardButton(
                    "Сброс истории",
                    callback_data="reset_history",
                )
            ],
            [
                InlineKeyboardButton(
                    "Обновить свою анкету",
                    callback_data="request_full_name",
                )
            ]
        ]
    try:
        query = update.callback_query
        query.answer()
        if message != query.message.text:
            query.edit_message_text(
                message,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
    except Exception:
        context.user_data['last_message'].edit_text(
            message,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


# Начальная точка модуля "Знакомства"
def comrad_search(update: Update, context: CallbackContext):
    participant = context.user_data["participant"]
    current_meetup = context.user_data["current_meetup"]
    is_communicative = check_questionnaire(participant, current_meetup.id)
    if is_communicative:
        show_questionnaires(update, context)
    else:
        inform_questionnaire(update, context)


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        CallbackQueryHandler(comrad_search, pattern="^comrad_search$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(
            show_questionnaires, pattern="^show_questionnaires$"
        )
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(reset_history, pattern="^reset_history$")
    )
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    request_full_name, pattern="^request_full_name$"
                )
            ],
            states={
                "FULL_NAME": [
                    CallbackQueryHandler(
                        get_full_name, pattern="^skip_full_name$"
                    ),
                    MessageHandler(
                        Filters.text & ~Filters.command, get_full_name
                    ),
                ],
                "STACK": [
                    MessageHandler(
                        Filters.text & ~Filters.command, get_stack
                    )
                ],
                "BIO": [
                    MessageHandler(
                        Filters.text & ~Filters.command, get_bio
                    )
                ]
            },
            fallbacks=[],
        )
    )
    return updater.dispatcher
