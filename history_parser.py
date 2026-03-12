import config
import keywords
import filters
from sender import send_lead


async def parse_history(client):
    print("📚 Парсим историю...")

    for group in config.SOURCE_GROUPS:
        try:
            async for message in client.iter_messages(group, limit=500):
                if not message or not message.text:
                    continue

                text = message.text.lower()

                for word in keywords.KEYWORDS:
                    if word in text:
                        result = filters.classify(text)

                        sender = await message.get_sender()
                        if not sender:
                            user = "неизвестный пользователь"
                        elif sender.username:
                            user = f"https://t.me/{sender.username}"
                        else:
                            user = f"id:{sender.id}"

                        chat = await message.get_chat()
                        chat_name = chat.title if chat else "неизвестная группа"

                        # ссылка
                        if chat and chat.username:
                            link = f"https://t.me/{chat.username}/{message.id}"
                        else:
                            link = None  # ссылки нет

                        message_text = f"📢 Группа: {chat_name}\n\n💬 Сообщение:\n{text}\n\n👤 Автор: {user}"
                        if link:
                            message_text += f"\n\n🔗 Ссылка: {link}"

                        topic_id = config.TOPICS["hot"] if result == "HOT" else config.TOPICS["cold"]

                        await send_lead(
                            client,
                            config.FORUM_ID,
                            topic_id,
                            message_text,
                            link if link else "",
                            user
                        )

                        break
        except Exception as e:
            print(f"Ошибка при парсинге группы {group}:", e)

    print("✅ История обработана")