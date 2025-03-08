from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask, request
from pymongo import MongoClient
import os
import threading
import asyncio

TOKEN = "8077840807:AAE9COv3o-3ffgLXr-XzZhskHG4PEhkDXQI"
IMAGE_URL = "https://envs.sh/Ed4.jpg"
OWNER_LINK = "https://t.me/rishu1286"
SUPPORT_LINK = "https://t.me/vip_robotz"
GROUP_LINK = "https://t.me/rishusupport"
MONGO_URI = "mongodb+srv://Krishna:pss968048@cluster0.4rfuzro.mongodb.net/?retryWrites=true&w=majority"
ADMIN_CHAT_ID = 6258915779  # Admin Telegram ID

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
    username = update.message.from_user.username or "No Username"
    
    # Check if user already exists
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id, "chat_id": chat_id, "first_name": first_name, "username": username})
        await context.bot.send_message(chat_id, "✅ A new user has joined!")
        
        # Notify admin asynchronously
        asyncio.create_task(context.bot.send_message(ADMIN_CHAT_ID, f"🚀 New user joined: {first_name} (@{username}) (ID: {user_id})"))
    
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

async def broadcast(update: Update, context):
    if update.message.chat_id != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ You are not authorized to send a broadcast.")
        return
    
    users = users_collection.find()
    broadcast_message = update.message.text.replace("/broadcast", "").strip()
    if not broadcast_message:
        await update.message.reply_text("❌ Please provide a message to broadcast.")
        return
    
    sent_count = 0
    failed_count = 0
    
    for user in users:
        chat_id = user.get("chat_id")
        if chat_id:
            try:
                await context.bot.send_message(chat_id=chat_id, text=broadcast_message)
                sent_count += 1
            except Exception as e:
                print(f"Failed to send message to {chat_id}: {e}")
                failed_count += 1
    
    await update.message.reply_text(f"✅ Broadcast sent successfully!\n📤 Sent: {sent_count}\n❌ Failed: {failed_count}")

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(telegram_app.run_polling())

if __name__ == "__main__":
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.ALL & filters.UpdateType.EDITED_MESSAGE, message_edit))
    telegram_app.add_handler(CommandHandler("broadcast", broadcast))
    
    # Start Telegram bot in a separate thread
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Run Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
