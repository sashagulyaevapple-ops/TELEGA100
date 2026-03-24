from telethon import TelegramClient
import config
import asyncio

client = TelegramClient(
    config.SESSION_NAME,
    config.API_ID,
    config.API_HASH
)


async def send_to_bot_async(text, topic_id):
    await client.connect()

    msg = await client.send_message(
        config.FORUM_ID,
        text,
        reply_to=topic_id
    )

    return msg


def send_to_bot(text, topic_id):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(send_to_bot_async(text, topic_id))


async def delete_message(message_id):
    await client.connect()
    await client.delete_messages(config.FORUM_ID, message_id)


async def send_to_topic(text, topic_id):
    await client.connect()
    await client.send_message(config.FORUM_ID, text, reply_to=topic_id)