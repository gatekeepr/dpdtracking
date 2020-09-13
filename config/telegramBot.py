from telegram.ext import Updater, CommandHandler

TOKEN_FILENAME = 'betterTrackingBotToken.pw'

# telegram driver
token = open(TOKEN_FILENAME, "r").read().strip()
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher