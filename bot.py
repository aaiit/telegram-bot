import os

# url_model = os.environ.get('URL_MODEL', None)
TOKEN =  os.environ.get('TELEGRAM_TOKEN', None)
web_url = os.environ.get('WEB_URL', None) # https://calm-sea.herokuapp.com/


# os.system("""
#     until $(curl -o Bot_Model.zip  %s); do
#     printf '.'
#     sleep 0.5
# done"""%(url_model))
# os.system("unzip Bot_Model.zip")


# from model import predict

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def info(update,context):
    user = update.message.from_user
    update.message.reply_text('You are the user {} and your user ID: {} '.format(user['username'], user['id']))


def reply(update, context):
    text = update.message.text
    #update.message.reply_text(update.message.text)
    #update.message.reply_photo(photo='https://telegram.org/img/t_logo.png') # replay to bot
    # update.message.reply_photo(open("downloand.png","rb"))
    # user = update.message.from_user
    # print(user)
    # update.message.reply_text(text)
    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("info", info))

    # on noncommand i.e message - reply the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, reply))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(web_url + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()