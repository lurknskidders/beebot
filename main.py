import requests
import time

TOKEN = "8476228733:AAGV3gPfzFFtxJdb6-CkJhoO7LPgYtXN-GU"
API_URL = f"https://api.telegram.org/bot{TOKEN}"
BEE_MOVIE_URL = 'https://gist.githubusercontent.com/MattIPv4/045239bc27b16b2bcf7a3a9a4648c08a/raw'

def get_latest_chat_id():
    resp = requests.get(f"{API_URL}/getUpdates")
    data = resp.json()
    if not data['ok'] or len(data['result']) == 0:
        print("No updates found yet. Send a message to the bot in the group to register chat_id.")
        return None
    # Take the last message chat id
    for update in reversed(data['result']):
        message = update.get('message')
        if message:
            chat = message.get('chat')
            if chat:
                chat_id = chat.get('id')
                print(f"Found chat_id: {chat_id}")
                return chat_id
    return None

def send_message(chat_id, text):
    resp = requests.post(f"{API_URL}/sendMessage", data={"chat_id": chat_id, "text": text})
    if resp.status_code != 200:
        print(f"Failed to send message: {resp.status_code} - {resp.text}")

def main():
    lines = requests.get(BEE_MOVIE_URL).text.strip().splitlines()
    chat_id = None
    print("Waiting for messages to get chat_id...")
    while chat_id is None:
        chat_id = get_latest_chat_id()
        if chat_id is None:
            time.sleep(5)  # wait a bit and try again

    print("Starting to send Bee Movie lines every hour...")
    for idx, line in enumerate(lines):
        send_message(chat_id, line)
        print(f"Sent line {idx+1}/{len(lines)}")
        time.sleep(3600)  # 1 hour delay

if __name__ == "__main__":
    main()
