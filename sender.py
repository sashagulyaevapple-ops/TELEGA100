import asyncio
import random
from telethon.errors import FloodWaitError

async def send_lead(client, forum_id, topic_id, text, link, user):
    """
    Отправка лида в форум.
    topic_id — ID темы форума (HOT/COLD/…)
    """
    message = text

    # антибан задержка
    delay = random.randint(10, 25)
    print(f"⏳ Антибан пауза {delay} сек")
    await asyncio.sleep(delay)

    try:
        # проверяем, есть ли topic_id
        if topic_id:
            # отправка в нужную тему форума
            await client.send_message(
                forum_id,
                message,
                reply_to=topic_id  # старый способ, который работал у тебя
            )
        else:
            await client.send_message(forum_id, message)

        print(f"✅ Лид отправлен в тему {topic_id}")

    except FloodWaitError as e:
        print(f"🚫 FloodWait {e.seconds} сек")
        await asyncio.sleep(e.seconds + 5)
        await client.send_message(forum_id, message)