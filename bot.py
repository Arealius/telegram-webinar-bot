import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import telegram

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает!")

async def reset_webhook(app):
    await app.bot.delete_webhook(drop_pending_updates=True)

app = ApplicationBuilder().token(TOKEN).post_init(reset_webhook).build()
app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    print("🚀 Запускаем бота в режиме polling...")
    app.run_polling()
