from telegram import Bot

async def send_telegram_message(message):
    token = ''
    chat_ids = ['']
    bot = Bot(token=token)
    for chat_id in chat_ids:
        await bot.send_message(chat_id=chat_id, text=message)
