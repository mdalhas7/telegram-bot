import os
import logging
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Telegram Token & DeepSeek API Key
TELEGRAM_TOKEN = os.environ['BOT_TOKEN']
DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

# /start কমান্ড হ্যান্ডলার
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👋 হ্যালো {update.effective_user.first_name}! আমি DeepSeek AI bot। আপনি এখন প্রশ্ন করতে পারেন।")

# মেসেজ হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "deepseek-chat",  # deepseek-coder/chat বা deepseek-chat উভয় ব্যবহারযোগ্য
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            }

            async with session.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload) as response:
                result = await response.json()
                reply = result['choices'][0]['message']['content']
                await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("⚠️ কিছু একটা ভুল হয়েছে।")
        logging.error(f"DeepSeek API Error: {e}")

# অ্যাপ রান করানো
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running with DeepSeek API...")
    app.run_polling()
    
