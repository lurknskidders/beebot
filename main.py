import os
import random
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

BOT_TOKEN = os.getenv("8476228733:AAGxTOE5ZSqqkeCW9HxQAAPSmVJB84tdfbU")
SCRIPT_URL = 'https://gist.githubusercontent.com/MattIPv4/045239bc27b16b2bcf7a3a4648c08a/raw'

def fetch_bee_lines():
    txt = requests.get(SCRIPT_URL).text
    lines = [line.strip() for line in txt.splitlines() if line.strip() and '-' not in line]
    return lines

bee_lines = fetch_bee_lines()
active_chats = set()

async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if cid not in active_chats:
        active_chats.add(cid)
        await context.bot.send_message(chat_id=cid, text="🐝 Bee Movie bot activated. Expect random lines.")
    else:
        await context.bot.send_message(chat_id=cid, text="✅ Already activated.")

async def send_random_line(app):
    while True:
        for cid in list(active_chats):
            msg = random.choice(bee_lines)
            await app.bot.send_message(chat_id=cid, text=msg)
        await asyncio.sleep(3600)  # 1 hour

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", activate))
    asyncio.create_task(send_random_line(app))
    print("🐝 Bee Movie bot running.")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
