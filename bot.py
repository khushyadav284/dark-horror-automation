import os
import json
import urllib.request
import time

TOKEN = os.environ["BOT_TOKEN"]
URL = f"https://api.telegram.org/bot{TOKEN}/"

def send(chat_id, text, keyboard=None):
    data = {"chat_id": chat_id, "text": text}
    if keyboard:
        data["reply_markup"] = {"inline_keyboard": keyboard}

    req = urllib.request.Request(
        URL + "sendMessage",
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req)

def main():
    offset = 0

    while True:
        try:
            req = urllib.request.urlopen(
                URL + f"getUpdates?offset={offset}&timeout=30"
            )
            updates = json.loads(req.read())["result"]

            for update in updates:
                offset = update["update_id"] + 1

                if "message" in update:
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]

                    if msg.get("text") == "/start":
                        keyboard = [
                            [{"text": "🎬 Complete Horror Video",
                              "callback_data": "video"}],
                            [{"text": "📖 Story + Voice + Images",
                              "callback_data": "story"}],
                            [{"text": "📤 YouTube Upload",
                              "callback_data": "upload"}]
                        ]
                        send(chat_id, "👻 Welcome to Dark Horror AI!\n\nChoose your option:", keyboard)

                elif "callback_query" in update:
                    q = update["callback_query"]
                    chat_id = q["message"]["chat"]["id"]
                    choice = q["data"]

                    messages = {
                        "video": "🎬 Complete video generation selected!",
                        "story": "📖 Story + Voice + Images selected!",
                        "upload": "📤 YouTube upload option selected!"
                    }

                    send(chat_id, messages.get(choice, "Choose an option."))

        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    main()
