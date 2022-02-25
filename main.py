import logging
import re
from telegram import Update, bot
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    Updater, MessageHandler, Filters,
)
import email_sender

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
group_id = 123456789 # group id goes here, to obtain it add bot o administrators and go to https://api.telegram.org/botTOKEN/getUpdates and get chat id there
updater = Updater("bot_token_goes_here")


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Enter your @ucu.edu.ua email address. We will send you an email with invitation link"
    )


def is_valid_email(email: str) -> bool:
    return re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email) and email.endswith('@ucu.edu.ua')


def echo(update: Update, context: CallbackContext) -> None:
    if is_valid_email(update.message.text):
        email_sender.send_text(update.message.text, f'Subject: UCU Auth\n\nHi from UCU Authentication: this is your link (it only works one time) - {updater.bot.create_chat_invite_link(chat_id=group_id, member_limit=1)["invite_link"]}')
        update.message.reply_text(f'Invitation link sent to {update.message.text}')
    else:
        update.message.reply_text('It is not a valid @ucu.edu.ua email')


def main() -> None:
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
