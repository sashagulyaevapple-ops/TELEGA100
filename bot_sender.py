import requests
import config

BASE_URL = f"https://api.telegram.org/bot{config.BOT_TOKEN}"


def send_to_bot(text, topic_id):

    payload = {
        "chat_id": config.BOT_CHAT_ID,
        "text": text,
        "message_thread_id": topic_id,
        "disable_web_page_preview": True
    }

    requests.post(f"{BASE_URL}/sendMessage", data=payload)


def delete_message(message_id):

    payload = {
        "chat_id": config.BOT_CHAT_ID,
        "message_id": message_id
    }

    requests.post(f"{BASE_URL}/deleteMessage", data=payload)


def send_to_topic(text, topic_id):

    payload = {
        "chat_id": config.BOT_CHAT_ID,
        "text": text,
        "message_thread_id": topic_id
    }

    requests.post(f"{BASE_URL}/sendMessage", data=payload)