from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ✅ /start কমান্ডে স্বাগতম বার্তা
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"আসসালামু আলাইকুম {user_name}!\nআপনাকে আমাদের গ্রুপে স্বাগতম 🤝"
    )

# ✅ স্বয়ংক্রিয় মেসেজ রিপ্লাই (সালাম + প্রশ্ন উত্তর)
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

# ✅ বট চালু করা
def main():
    app = Application.builder().token("BOT_TOKEN").build()

    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    app.run_polling()

if __name__ == "__main__":
    main()
