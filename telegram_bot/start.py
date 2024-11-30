from telegram import (
    InlineKeyboardButton,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Updater,
)

from .common.db_querrys import (
    check_participant,
    create_participant,
    get_actual_meetups,
    get_meetup,
    get_planning_speech
)

from .common.extra_funcs import (
    safe_send_message
)


# Регистрация пользователя
def reg_user(update: Update, context: CallbackContext):
    user = update.message.from_user
    if not check_participant(user["id"]):
        create_participant(
            user["id"],
            user["first_name"],
            user["last_name"],
            user["username"],
        )


# Старт бота. Выбираем актуальный митап.
def start(update: Update, context: CallbackContext):
    context.user_data.clear()
    context.user_data["client_id"] = update.effective_chat.id
    if not check_participant(context.user_data["client_id"]):
        reg_user(update, context)
    actual_meetups = get_actual_meetups()
    if actual_meetups.count() == 0:
        no_meetups_message = "К сожалению, в ближайшее время митапы не запланированы.\nОжидайте информационную рассылку в боте!"
        safe_send_message(update, no_meetups_message)
    elif actual_meetups.count() == 1:
        only_one_meetup_message = "На данный момент доступен лишь один митап на выбор. Выбран автоматически."
        context.bot.send_message(
            text=only_one_meetup_message, chat_id=update.effective_chat.id
        )
        context.user_data["current_meetup"] = actual_meetups.first()
        menu(update, context)
    else:
        buttons = [
            [InlineKeyboardButton(
                f"{meetup.title}  {format(meetup.date, '%B %d')}",
                callback_data=f"meetup_id_{meetup.id}",
            )]
            for meetup in actual_meetups
        ]
        start_message = 'Добро пожаловать.\nВыберите, пожалуйста, интересующий Вас митап.'
        safe_send_message(update, start_message, buttons)


# Выбор митапа, если их больше одного
def show_meetups(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if not context.user_data.get("meetup_id"):
        context.user_data["meetup_id"] = query.data.split("_")[-1]
    current_meetup = get_meetup(context.user_data["meetup_id"])
    context.user_data["current_meetup"] = current_meetup
    context.user_data["planning_speech"] = get_planning_speech(
        context.user_data["client_id"], current_meetup.id
    )
    menu(update, context)


# Меню пользователя
def menu(update: Update, context: CallbackContext):
    is_speaker = bool(context.user_data["planning_speech"])
    speaker_button = [InlineKeyboardButton(
        "Начать выступление", callback_data="speech_speaker"
    )]
    # ===================  TO DO ===================
    # question_button = [InlineKeyboardButton(
    #     "Задать вопрос докладчику", callback_data="speech_questions"
    # )]
    buttons = [
        [InlineKeyboardButton("Расписание", callback_data="schedule")],
        [InlineKeyboardButton("Знакомства", callback_data="comrad_search")],
        [InlineKeyboardButton("Поддержать организатора!", callback_data="donate")],
        [InlineKeyboardButton("Выбрать митап", callback_data="start")],
    ]
    if is_speaker:
        buttons = [speaker_button] + buttons

    # ===================  TO DO ===================
    # if is_active_speaker:
    #   buttons = [question_button] + buttons
    meetup = context.user_data["current_meetup"]
    menu_message = f'Приветствуем!\n{meetup.title}\nДата: {format(meetup.date, "%c")}\nАдрес: {meetup.address}\n\nВыберите интересующий пункт меню'
    safe_send_message(update, menu_message, buttons)


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(start, pattern="^start$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(reg_user, pattern="^reg_user$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(show_meetups, pattern="^meetup_id_")
    )
    return updater.dispatcher
