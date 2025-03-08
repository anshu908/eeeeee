from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

TOKEN = "8077840807:AAE9COv3o-3ffgLXr-XzZhskHG4PEhkDXQI"
IMAGE_URL = "https://envs.sh/wf4.jpg"  # Change to your image URL
OWNER_LINK = "https://t.me/your_owner"
SUPPORT_LINK = "https://t.me/your_support"
GROUP_LINK = "https://t.me/your_group"

async def start(update: Update, context):
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

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & filters.UpdateType.EDITED_MESSAGE, message_edit))
    print("Bot is running...")
    app.run_polling()
