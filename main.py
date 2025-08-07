import logging
import requests
import schedule
import time
import threading
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

TOKEN = '8476228733:AAGV3gPfzFFtxJdb6-CkJhoO7LPgYtXN-GU'

# Load Bee Movie lines from Gist
BEE_MOVIE_URL = 'https://gist.githubusercontent.com/MattIPv4/045239bc27b16b2bcf7a3a9a4648c08a/raw'
lines = requests.get(BEE_MOVIE_URL).text.strip().splitlines()

# Dict to track progress per chat
chat_progress = {}

def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id not in chat_progress:
        chat_progress[chat_id] = 0
        context.bot.send_message(chat_id, "Bee Movie bot is now active in this chat.")

def send_line(context: CallbackContext):
    for chat_id in chat_progress:
        index = chat_progress[chat_id]
        if index < len(lines):
            context.bot.send_message(chat_id, lines[index])
            chat_progress[chat_id] += 1
        else:
            chat_progress[chat_id] = 0  # restart

def run_schedule(context: CallbackContext):
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Any message triggers registration
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

    # Send a line every hour to all registered chats
    schedule.every().hour.do(send_line, context=updater.bot)

    threading.Thread(target=run_schedule, args=(updater.bot,), daemon=True).start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
