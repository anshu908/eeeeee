from flask import Flask
from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import TOKEN, OWNER_ID
import threading

app = Flask(__name__)

def start(update: Update, context: CallbackContext):
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

    context.bot.send_photo(chat_id=update.effective_chat.id, 
                            photo="https://te.legra.ph/file/5a9550c10d934ff11f7b8.jpg")
    update.message.reply_text(f"Hello! {mention}! I am Edit Guardian bot I delete Edited messages", 
                              reply_markup=InlineKeyboardMarkup(keyboard))

def check_edit(update: Update, context: CallbackContext):
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
    
    bot.send_message(chat_id=chat_id, text=f"{user_mention} just edited a message🤡. I deleted their edited message🙂‍↕️🤡.")
    bot.delete_message(chat_id=chat_id, message_id=message_id)

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.update.edited_message, check_edit))
    
    updater.start_polling()
    updater.idle()

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host='0.0.0.0', port=8080)
