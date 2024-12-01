from django.conf import settings
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from .common.db_querrys import create_donation
from .start import menu


def amount_request(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    buttons = [
        [
            InlineKeyboardButton(
                "В меню",
                callback_data="to_menu",
            )
        ]
    ]

    query.edit_message_text(
        "Введите сумму пожертвования",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return "DONATE"


def donate(update: Update, context: CallbackContext):
    amount = update.message.text
    if not amount.isnumeric():
        update.message.reply_text("Сумма должна быть числом")
        return
    if int(amount) < 10:
        update.message.reply_text("Сумма должна быть больше 10 руб.")
        return

    invoice_amount = amount + "00"
    meetup = context.user_data["current_meetup"]
    donor = context.user_data["participant"]
    create_donation(meetup, donor, int(amount))

    context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title="Оплата",
        description="Сделать пожертвование",
        provider_token=settings.PAYMENT_TOKEN,
        currency="RUB",
        payload="donate",
        prices=[LabeledPrice(label="title", amount=int(invoice_amount))],
    )


def to_menu(update: Update, context: CallbackContext):
    menu(update, context)
    return ConversationHandler.END


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    amount_request, pattern="^donate$"
                )
            ],
            states={
                "DONATE": [
                    MessageHandler(
                        Filters.text & ~Filters.command, donate
                    ),
                ]
            },
            fallbacks=[CallbackQueryHandler(to_menu, pattern="^to_menu$")],
        )
    )
    return updater.dispatcher
