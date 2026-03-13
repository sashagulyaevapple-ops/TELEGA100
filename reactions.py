from telethon import events
from telethon.tl.types import PeerChannel, PeerChat, PeerUser
import config
from bot_sender import delete_message, send_to_topic

async def handle_reactions(client):
    """
    Ловим реакции на сообщения в форуме.
    Аккаунт Telethon слушает события UpdateMessageReactions.
    Действия выполняет бот.
    """
    @client.on(events.Raw)
    async def reaction_handler(event):
        if event.__class__.__name__ != "UpdateMessageReactions":
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

            # проверяем, что событие в нужном форуме
            if chat_id != config.FORUM_ID:
                return

            message_id = event.msg_id

            # получаем текст сообщения
            message = await client.get_messages(chat_id, ids=message_id)
            if not message or not message.text:
                return
            text = message.text

            # перебираем все новые реакции
            for r in event.reactions.recent_reactions:
                emoji = r.reaction.emoticon

                # 💩 удалить сообщение
                if emoji == "💩":
                    delete_message(message.id)
                    print(f"💩 Лид удален: {text[:50]}...")

                # 🎉 отправить в BEST
                elif emoji == "🎉":
                    send_to_topic(text, config.TOPICS["best"])
                    print(f"🎉 Лид отправлен в BEST: {text[:50]}...")

                # 🕊 отправить в WORK
                elif emoji == "🕊":
                    send_to_topic(text, config.TOPICS["work"])
                    print(f"🕊 Лид отправлен в WORK: {text[:50]}...")

                # логируем все реакции
                send_to_topic(
                    f"Новая реакция {emoji} на сообщение:\n{text}",
                    config.TOPICS["reactions"]
                )

        except Exception as e:
            print("Ошибка реакции:", e)