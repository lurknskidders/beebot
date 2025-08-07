import requests
import asyncio

TOKEN = "8476228733:AAGV3gPfzFFtxJdb6-CkJhoO7LPgYtXN-GU"  # <- paste your bot token here!
API_URL = f"https://api.telegram.org/bot{TOKEN}"
BEE_MOVIE_URL = 'https://gist.githubusercontent.com/MattIPv4/045239bc27b16b2bcf7a9a4648c08a/raw'

lines = requests.get(BEE_MOVIE_URL).text.strip().splitlines()

chat_progress = {}
registered_chats = set()

async def get_updates(offset=None):
    params = {"timeout": 100, "offset": offset}
    resp = requests.get(f"{API_URL}/getUpdates", params=params)
    return resp.json()

def send_message(chat_id, text):
    requests.post(f"{API_URL}/sendMessage", data={"chat_id": chat_id, "text": text})

async def main_loop():
    offset = None
    while True:
        updates = await get_updates(offset)
        if updates.get("ok"):
            for update in updates["result"]:
                offset = update["update_id"] + 1
                message = update.get("message")
                if message:
                    chat_id = message["chat"]["id"]
                    if chat_id not in registered_chats:
                        registered_chats.add(chat_id)
                        chat_progress[chat_id] = 0
                        send_message(chat_id, "🐝 Bee Movie Bot activated! One line per hour.")

        for chat_id in list(registered_chats):
            idx = chat_progress.get(chat_id, 0)
            if idx < len(lines):
                send_message(chat_id, lines[idx])
                chat_progress[chat_id] = idx + 1
            else:
                chat_progress[chat_id] = 0

        await asyncio.sleep(3600)  # wait 1 hour

if __name__ == "__main__":
    asyncio.run(main_loop())
