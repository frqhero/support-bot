import os

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    Filters,
)

from contact_dialogflow import detect_intent_texts
from logging_handler import TelegramLogsHandler


def error_handler(update: object, context: CallbackContext) -> None:
    context.bot.logger.warning(context.error)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        rf'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    is_fallback, response_text = detect_intent_texts(
        project_id, update.message.chat_id, update.message.text, 'RU'
    )
    if not is_fallback:
        update.message.reply_text(response_text)


def main() -> None:
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(telegram_token)
    bot = updater.bot
    tg_chat_id = os.getenv('TG_CHAT_ID_SEND_ERRORS_TO')
    bot.logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))
    bot.logger.warning('Dialogflow bot via tg has been started')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo)
    )

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    project_id = os.getenv('PROJECT_ID')
    main()
