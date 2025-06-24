import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# লোগিং (Debug করার জন্য)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# API Key পরিবেশ থেকে নাও
TELEGRAM_TOKEN = os.environ['BOT_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# OpenAI ক্লায়েন্ট তৈরি করো
client = OpenAI(api_key=OPENAI_API_KEY)

# /start কমান্ড হ্যান্ডলার
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"👋 হ্যালো ❄️{user_name}!\nআমাকে কিছু জিজ্ঞেস করো, আমি AI দিয়ে উত্তর দিব!")

# মেসেজ হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # বা চাইলে "gpt-4"
            messages=[
                {"role": "system", "content": "তুমি একজন সহায়ক AI অ্যাসিস্ট্যান্ট।"},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"❌ GPT তে সমস্যা: {e}")
        await update.message.reply_text("❌ কিছু সমস্যা হয়েছে! পরে আবার চেষ্টা করো।")

# অ্যাপ চালু করো
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()
    
