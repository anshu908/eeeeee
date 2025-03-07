from flask import Flask
from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio
from config import TOKEN, OWNER_ID

app = Flask(__name__)

async def start(update: Update, context):
    user = update.effective_user
    mention = f"{user.first_name}"
    keyboard = [
        [
            InlineKeyboardButton("Source Code", url="https://github.com/rishubot"),
            InlineKeyboardButton("Support Chat", url="https://t.me/ur_rishu_143")
        ],
        [
            InlineKeyboardButton("Add me to group", url="https://t.me/FakeTriedBot?startgroup=true")
        ],
        [
            InlineKeyboardButton("Owner", url="https://t.me/rishu1286"),
        ]
    ]

    await context.bot.send_photo(chat_id=update.effective_chat.id, 
                            photo="https://te.legra.ph/file/5a9550c10d934ff11f7b8.jpg")
    
    await update.message.reply_text(f"Hello! {mention}! I am Edit Guardian bot I delete Edited messages", 
                              reply_markup=InlineKeyboardMarkup(keyboard))

async def check_edit(update: Update, context):
    bot: Bot = context.bot
    edited_message = update.edited_message
    if not edited_message:
        return

    chat_id = edited_message.chat_id
    message_id = edited_message.message_id
    user_id = edited_message.from_user.id
    user_mention = f"{edited_message.from_user.first_name}"
    
    if user_id == OWNER_ID:
        return  # Ignore if owner edits the message
    
    await bot.send_message(chat_id=chat_id, text=f"{user_mention} just edited a message🤡. I deleted their edited message🙂‍↕️🤡.")
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

async def run_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, check_edit))

    await application.run_polling()

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())  # Telegram bot ko async run karne ke liye
    app.run(host='0.0.0.0', port=8080)
