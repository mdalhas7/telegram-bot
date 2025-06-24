import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import openai

# লোগিং (ডিবাগging-এর জন্য)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# API Key গুলো পরিবেশ ভেরিয়েবল থেকে নাও
TELEGRAM_TOKEN = os.environ['BOT_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# OpenAI কনফিগার
openai.api_key = OPENAI_API_KEY

# /start কমান্ড
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"👋 হ্যালো {user_name}! আমাকে কিছু জিজ্ঞেস করো, আমি AI দিয়ে উত্তর দিব!")

# মেসেজের উত্তর GPT দিয়ে
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # বা অন্য যেটা তুমি ব্যবহার করতে চাও
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("❌ কিছু সমস্যা হয়েছে! পরে আবার চেষ্টা করো।")
        logging.error(e)

# মূল অংশ
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
    
