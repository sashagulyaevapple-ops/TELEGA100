from telethon import TelegramClient, events
import asyncio
import random

import config
import keywords
import filters
from reactions import handle_reactions
from bot_sender import send_to_bot

processed_messages = set()
MAX_CACHE = 5000

client = TelegramClient(
    config.SESSION_NAME,
    config.API_ID,
    config.API_HASH
)

@client.on(events.NewMessage(chats=config.SOURCE_GROUPS))
async def handler(event):
    try:
        if not event.raw_text:
            return

        text = event.raw_text.lower()

        # проверка стоп слов
        for stop_word in keywords.STOP_KEYWORDS:
            if stop_word in text:
                print("🚫 Найдено стоп слово:", stop_word)
                return

        unique_id = f"{event.chat_id}_{event.id}"

        if unique_id in processed_messages:
            return

        processed_messages.add(unique_id)

        if len(processed_messages) > MAX_CACHE:
            processed_messages.clear()

        print("📩 Новое сообщение:", text[:100])

        # проверка ключевых слов
        keyword_found = False

        for word in keywords.KEYWORDS:
            if word in text:
                keyword_found = True
                print("🔎 Найден ключ:", word)
                break

        if not keyword_found:
            return

        # проверка лид слов
        lead_found = False

        for lead_word in keywords.LEAD_WORDS:
            if lead_word in text:
                lead_found = True
                print("🔥 Найден лид триггер:", lead_word)
                break

        result = filters.classify(text)

        if result == "SPAM":
            print("⛔ Спам пропущен")
            return

        if lead_found:
            result = "HOT"

        sender = await event.get_sender()

        if not sender:
            user = "неизвестный пользователь"
        elif sender.username:
            user = f"https://t.me/{sender.username}"
        else:
            user = f"id:{sender.id}"

        chat = await event.get_chat()

        chat_name = chat.title if chat else "неизвестная группа"

        # ссылка на сообщение
        if chat.username:
            link = f"https://t.me/{chat.username}/{event.id}"
        else:
            chat_id_short = str(chat.id)[4:]
            link = f"https://t.me/c/{chat_id_short}/{event.id}"

        message_text = f"📢 Группа: {chat_name}\n\n💬 Сообщение:\n{text}\n\n👤 Автор: {user}"

        if link:
            message_text += f"\n\n🔗 Ссылка: {link}"

        await asyncio.sleep(random.uniform(2, 5))

        topic_id = config.TOPICS["hot"] if result == "HOT" else config.TOPICS["cold"]

        print("🔥 ГОРЯЧИЙ ЛИД" if result == "HOT" else "❄️ ХОЛОДНЫЙ ЛИД")

        # отправка через бота
        send_to_bot(message_text, topic_id)

    except Exception as e:
        print("Ошибка:", e)


print("🚀 Подключаем Telegram...")

client.start()

print("✅ Telegram подключен")
print("👀 Парсер слушает группы в реальном времени")

# регистрация обработчика реакций
handle_reactions(client)

client.run_until_disconnected()