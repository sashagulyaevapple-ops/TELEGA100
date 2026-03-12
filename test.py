from telethon import TelegramClient, events

api_id = 33952778
api_hash = "1ff5e330510e351f44aca548d49bc0e9"

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    print("Новое сообщение:", event.raw_text)

client.start()
print("Скрипт работает...")
client.run_until_disconnected()