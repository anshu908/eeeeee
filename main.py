from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask, request
from pymongo import MongoClient
import os
import threading

TOKEN = "8077840807:AAE9COv3o-3ffgLXr-XzZhskHG4PEhkDXQI"
IMAGE_URL = "https://envs.sh/wf4.jpg"
OWNER_LINK = "https://t.me/your_owner"
SUPPORT_LINK = "https://t.me/your_support"
GROUP_LINK = "https://t.me/your_group"
MONGO_URI = "mongodb+srv://your_mongo_uri"

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["telegram_bot"]
users_collection = db["users"]

# Telegram Bot Setup
telegram_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    first_name = update.message.from_user.first_name
    
    # Check if user already exists
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id, "chat_id": chat_id, "first_name": first_name})
        await context.bot.send_message(chat_id, "✅ A new user has joined!")
    
    keyboard = [
        [InlineKeyboardButton("Owner", url=OWNER_LINK), InlineKeyboardButton("Support", url=SUPPORT_LINK)],
        [InlineKeyboardButton("Group", url=GROUP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(photo=IMAGE_URL, caption="Welcome to the bot!", reply_markup=reply_markup)

async def message_edit(update: Update, context):
    edited_message = update.edited_message
    if edited_message:
        chat_id = edited_message.chat_id
        user = edited_message.from_user
        text = f"⚠️ {user.mention_html()} ne ek message edit kiya!"
        await context.bot.send_message(chat_id, text, parse_mode="HTML")

async def broadcast_message(context, message):
    users = users_collection.find()
    for user in users:
        try:
            await context.bot.send_message(user["chat_id"], message)
        except Exception as e:
            print(f"Failed to send message to {user['chat_id']}: {e}")

@app.route("/broadcast", methods=["POST"])
def broadcast():
    data = request.json
    message = data.get("message")
    if message:
        threading.Thread(target=lambda: telegram_app.create_task(broadcast_message(telegram_app, message))).start()
        return {"status": "Broadcast started"}, 200
    return {"error": "Message is required"}, 400

if __name__ == "__main__":
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.ALL & filters.UpdateType.EDITED_MESSAGE, message_edit))
    
    # Start Telegram bot in a separate thread
    threading.Thread(target=telegram_app.run_polling, daemon=True).start()
    
    # Run Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
