import os
import re
import time
from collections import defaultdict
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
    ChatMemberHandler
)

# Get your bot token from environment variables
TOKEN = os.getenv("8266577753:AAGtF7PVgLJTagR9lgh9WlAhpypIumpqLiA")

# Store messages for anti-spam
user_messages = defaultdict(list)

# List of bad keywords (you can customize)
bad_words = ["casino", "gambling", "promo", "adult", "scam"]

# Function to check each message
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text

    if not message:
        return

    # Anti-link: only admins/owner can send links
    link_pattern = r"(https?://\S+|t\.me/\S+)"
    if re.search(link_pattern, message):
        member = await context.bot.get_chat_member(update.effective_chat.id, user.id)
        if member.status not in ["administrator", "creator"]:
            await update.message.delete()
            return

    # Anti-spam: max 5 messages in 5 seconds
    now = time.time()
    user_messages[user.id] = [t for t in user_messages[user.id] if now - t < 5]
    user_messages[user.id].append(now)
    if len(user_messages[user.id]) > 5:
        await update.message.delete()
        return

    # Bad word filter
    for word in bad_words:
        if word in message.lower():
            await update.message.delete()
            return

# Function to restrict new members from sending links
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            member.id,
            permissions={
                "can_send_messages": True,
                "can_send_other_messages": False,
                "can_add_web_page_previews": False
            }
        )

# Build the bot application
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), check_message))
app.add_handler(ChatMemberHandler(new_member, ChatMemberHandler.CHAT_MEMBER))

# Run the bot
app.run_polling()
