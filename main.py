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

# Get your bot token from environment variables (secure)
TOKEN = os.getenv(8266577753:AAGtF7PVgLJTagR9lgh9WlAhpypIumpqLiA)

# Store messages and offenses
user_messages = defaultdict(list)
bad_words = ["casino", "gambling", "promo", "scam"]  # customize as needed

# Check user messages
async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text

    if not message:
        return

    # Anti-link (only admins/owner allowed)
    link_pattern = r"(https?://\S+|t\.me/\S+)"
    if re.search(link_pattern, message):
        member = await context.bot.get_chat_member(update.effective_chat.id, user.id)
        if member.status not in ["administrator", "creator"]:
            await update.message.delete()
            return

    # Anti-spam (5 messages in 5 seconds)
    now = time.time()
    user_messages[user.id] = [t for t in user_messages[user.id] if now - t < 5]
