import requests

def send_telegram(bot_token, chat_id, text):
    if not bot_token or not chat_id:
        return False
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    for i in range(0, len(text), 3800):
        r = requests.post(
            url,
            json={"chat_id": chat_id, "text": text[i:i+3800]},
            timeout=30,
        )
        r.raise_for_status()
    return True
