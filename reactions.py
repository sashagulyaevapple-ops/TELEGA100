from telethon import events
from telethon.tl.types import PeerChannel, PeerChat, PeerUser, UpdateMessageReactions

import config
from bot_sender import delete_message, send_to_topic
from storage import message_map


async def handle_reactions(client):

    @client.on(events.Raw)
    async def reaction_handler(event):

        if not isinstance(event, UpdateMessageReactions):
            return

        try:
            # определяем chat_id
            if isinstance(event.peer, PeerChannel):
                chat_id = event.peer.channel_id

            elif isinstance(event.peer, PeerChat):
                chat_id = event.peer.chat_id

            elif isinstance(event.peer, PeerUser):
                chat_id = event.peer.user_id

            else:
                return

            # проверяем что это наш форум
            if chat_id != abs(config.FORUM_ID):
                return

            message_id = event.msg_id

            # 🔥 берём данные из кеша
            data = message_map.get(message_id)

            if not data:
                print("⚠️ Нет данных по сообщению")
                return

            text = data["text"]

            # проверка наличия реакций
            if not event.reactions:
                return

            if not event.reactions.recent_reactions:
                return

            for r in event.reactions.recent_reactions:

                emoji = r.reaction.emoticon

                # 💩 удалить
                if emoji == "💩":
                    await delete_message(message_id)
                    print("💩 Лид удален")

                # 🎉 BEST
                elif emoji == "🎉":
                    await send_to_topic(text, config.TOPICS["best"])
                    print("🎉 Лид отправлен в BEST")

                # 🕊 WORK
                elif emoji == "🕊":
                    await send_to_topic(text, config.TOPICS["work"])
                    print("🕊 Лид отправлен в WORK")

                # лог всех реакций
                await send_to_topic(
                    f"Новая реакция {emoji} на сообщение:\n{text}",
                    config.TOPICS["reactions"]
                )

        except Exception as e:
            print("Ошибка реакции:", e)