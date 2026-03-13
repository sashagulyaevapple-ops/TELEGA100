from telethon import events
from telethon.tl.types import PeerChannel, PeerChat, PeerUser, UpdateMessageReactions
import config
from bot_sender import delete_message, send_to_topic


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

            # проверяем форум
            if chat_id != abs(config.FORUM_ID):
                return

            message_id = event.msg_id

            message = await client.get_messages(config.FORUM_ID, ids=message_id)

            if not message or not message.text:
                return

            text = message.text

            if not event.reactions:
                return

            if not event.reactions.recent_reactions:
                return

            for r in event.reactions.recent_reactions:

                emoji = r.reaction.emoticon

                # 💩 удалить
                if emoji == "💩":

                    delete_message(message.id)

                    print("💩 Лид удален")

                # 🎉 BEST
                elif emoji == "🎉":

                    send_to_topic(text, config.TOPICS["best"])

                    print("🎉 Лид отправлен в BEST")

                # 🕊 WORK
                elif emoji == "🕊":

                    send_to_topic(text, config.TOPICS["work"])

                    print("🕊 Лид отправлен в WORK")

                # лог реакций
                send_to_topic(
                    f"Новая реакция {emoji} на сообщение:\n{text}",
                    config.TOPICS["reactions"]
                )

        except Exception as e:
            print("Ошибка реакции:", e)