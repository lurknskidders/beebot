import os
import requests
import asyncio

TOKEN = os.getenv("8476228733:AAGV3gPfzFFtxJdb6-CkJhoO7LPgYtXN-GU")
if not TOKEN:
    raise Exception("Missing TOKEN environment variable.")

API_URL = f"https://api.telegram.org/bot{TOKEN}"
BEE_MOVIE_URL = 'https://gist.githubusercontent.com/MattIPv4/045239bc27b16b2bcf7a3a9a4648c08a/raw'

lines = requests.get(BEE_MOVIE_URL).text.strip().splitlines()

chat_progress = {}
registered_chats = set()

# Get updates from Telegram (long polling)
async def get_updates(offset=None):
    params = {"timeout": 100, "offset": offset}
    resp = requests.get(f"{API_URL}/getUpdates", params=params)
    return resp.json()

# Send message to a chat
def send_message(chat_id, text):
    requests.post(f"{API_URL}/sendMessage", data={"chat_id": chat_id, "text": text})

async def main_loop():
    offset = None
    while True:
        updates = await get_updates(offset)
        if updates.get("ok"):
            for update in updates["result"]:
                offset = update["update_id"] + 1

                # Register any chat that sends a message
                message = update.get("message")
                if message:
                    chat_id = message["chat"]["id"]
                    if chat_id not in registered_chats:
                        registered_chats.add(chat_id)
                        chat_progress[chat_id] = 0
                        send_message(chat_id, "🍯 Bee Movie Bot activated! You'll now receive one line per hour.")

        # Send the next line to each chat
        for chat_id in list(registered_chats):
            idx = chat_progress.get(chat_id, 0)
            if idx < len(lines):
                send_message(chat_id, lines[idx])
                chat_progress[chat_id] = idx + 1
            else:
                chat_progress[chat_id] = 0  # loop again

        await asyncio.sleep(3600)  # 1 hour wait

if __name__ == "__main__":
    asyncio.run(main_loop())
