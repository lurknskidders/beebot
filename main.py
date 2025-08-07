import asyncio
import os
import random
import requests
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
)

# Get token from environment variable (use Railway's Variables section)
BOT_TOKEN = os.getenv("8476228733:AAGV3gPfzFFtxJdb6-CkJhoO7LPgYtXN-GU")
# Bee Movie script source
SCRIPT_URL = 'https://gist.githubusercontent.com/MattIPv4/045239bc27b16b2bcf7a3a9a4648c08a/raw'

# Fetch Bee Movie lines
def fetch_bee_lines():
    txt = requests.get(SCRIPT_URL).text
    lines = [line.strip() for line in txt.splitlines() if line.strip() and '-' not in line]
    return lines

bee_lines = fetch_bee_lines()
active_chats = set()

# /activate command
async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if cid not in active_chats:
        active_chats.add(cid)
        await context.bot.send_message(chat_id=cid, text="🐝 Bee Movie bot activated. Expect random lines hourly.")
    else:
        await context.bot.send_message(chat_id=cid, text="✅ Already activated.")

# Send Bee Movie lines every hour
async def random_bee_hourly(bot: Bot):
    while True:
        for cid in list(active_chats):
            msg = random.choice(bee_lines)
            await bot.send_message(chat_id=cid, text=msg)
        await asyncio.sleep(3600)  # Every hour

# Start bot
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("activate", activate))
    asyncio.create_task(random_bee_hourly(app.bot))
    print("🐝 Bee Movie bot running.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
