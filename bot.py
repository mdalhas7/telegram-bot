import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# Logging (ডিবাগিং এর জন্য)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# API Key গুলো এনভায়রনমেন্ট থেকে নেওয়া
TELEGRAM_TOKEN = os.environ['BOT_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# OpenAI Client তৈরি
client = OpenAI(api_key=OPENAI_API_KEY)

# /start কমান্ড হ্যান্ডলার
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"👋 হ্যালো {user_name}! আমি ChatGPT বট। আমাকে কিছু জিজ্ঞেস করো।")

# মেসেজ হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # চাইলে এখানে gpt-4 লিখতে পারো (তোমার অ্যাক্সেস থাকলে)
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        bot_reply = response.choices[0].message.content
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text("❌ কিছু একটা ভুল হয়েছে।")
        logging.error(f"Error: {e}")

# অ্যাপ রান করানো
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()
