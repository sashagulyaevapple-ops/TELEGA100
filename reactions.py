from telethon import events
import config


async def handle_reactions(client):

    @client.on(events.Raw)
    async def reaction_handler(event):

        # ловим только события реакций
        if event.__class__.__name__ != "UpdateMessageReactions":
            return

        try:

            chat_id = event.peer.channel_id
            message_id = event.msg_id

            # получаем сообщение
            message = await client.get_messages(chat_id, ids=message_id)

            if not message:
                return

            text = message.text

            # реакции
            for r in event.reactions.recent_reactions:

                emoji = r.reaction.emoticon

                # 💩 удалить
                if emoji == "💩":

                    await client.delete_messages(
                        config.FORUM_ID,
                        message.id
                    )

                    print("💩 Лид удален")

                # 🎉 лучшие
                elif emoji == "🎉":

                    await client.send_message(
                        config.FORUM_ID,
                        text,
                        reply_to=config.TOPICS["best"]
                    )

                    print("🎉 Лид отправлен в ЛУЧШИЕ")

                # 🕊 в работу
                elif emoji == "🕊":

                    await client.send_message(
                        config.FORUM_ID,
                        text,
                        reply_to=config.TOPICS["work"]
                    )

                    print("🕊 Лид отправлен В РАБОТУ")

                # лог реакций
                await client.send_message(
                    config.FORUM_ID,
                    f"Новая реакция {emoji}\n\n{text}",
                    reply_to=config.TOPICS["reactions"]
                )

        except Exception as e:

            print("Ошибка реакции:", e)