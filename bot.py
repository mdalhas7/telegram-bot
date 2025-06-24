import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# টোকেন Railway এর Variables থেকে নিবে
TOKEN = os.environ['BOT_TOKEN']

# /start কমান্ডে স্বাগত বার্তা
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"আসসালামু আলাইকুম {user_name}!\nআপনাকে আমাদের গ্রুপে স্বাগতম 🤝"
    )

# মেসেজ অনুযায়ী উত্তর দেওয়া
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower().strip()

    if "আসসালামু আলাইকুম" in msg or "assalamualaikum" in msg:
        await update.message.reply_text("وَعَلَيْكُمُ السَّلَامُ وَرَحْمَةُ ٱللّٰهِ وَبَرَكَاتُهُ 🌸")
        return

    if "মেইন চ্যানেল" in msg or "main channel" in msg:
        await update.message.reply_text("🔗 আমাদের মেইন চ্যানেল: https://t.me/HACKERA17X")
        return

    if "admin" in msg or "এডমিন" in msg or "এডমিন কে" in msg:
        await update.message.reply_text("👤 অ্যাডমিন: @MsSumaiyaKhanom")
        return

# মেইন ফাংশন: বট চালানো
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    app.run_polling()

if __name__ == "__main__":
    main()
