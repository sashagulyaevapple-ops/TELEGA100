import requests
import config


def send_to_bot(text, topic_id):

    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": config.BOT_CHAT_ID,
        "text": text,
        "message_thread_id": topic_id,
        "disable_web_page_preview": True
    }

    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print("Bot send error:", e)