import os
import asyncio
import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

# Load Telegram bot token from Railway environment variable
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise Exception("Missing TOKEN environment variable.")

# Load Bee Movie script lines from Gist (live)
BEE_MOVIE_URL = 'https://gist.githubusercontent.com/MattIPv4/045239bc27b16b2bcf7a3a9a4648c08a/raw'
lines = requests.get(BEE_MOVIE_URL).text.strip().splitlines()

# Track which line each chat has seen
chat_progress = {}

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Called when the bot sees any message in a chat
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in chat_progress:
        chat_progress[chat_id] = 0
        await context.bot.send_message(chat_id, "🍯 Bee Movie Bot activated! You'll now receive one line per hour.")

# Background job: sends a line from the movie every hour
async def send_line_periodically(application):
    while True:
        for chat_id in list(chat_progress.keys()):
            index = chat_progress[chat_id]
            if index < len(lines):
                try:
                    await application.bot.send_message(chat_id, lines[index])
                    chat_progress[chat_id] += 1
                except Exception as e:
                    logger.warning(f"Failed to send to {chat_id}: {e}")
            else:
                chat_progress[chat_id] = 0  # Restart from beginning
        await asyncio.sleep(3600)  # Wait 1 hour

# Main async entry point
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Listen for all text messages (to register groups/chats)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the background loop for sending messages
    asyncio.create_task(send_line_periodically(app))

    # Start the bot
    await app.run_polling()

# Start everything
if __name__ == "__main__":
    asyncio.run(main())
