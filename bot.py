import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://{HOSTNAME}{WEBHOOK_PATH}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("🌐 Устанавливаю webhook:", WEBHOOK_URL)

app.run_webhook(
    listen="0.0.0.0",
    port=8443,
    webhook_url=WEBHOOK_URL,
    webhook_path=WEBHOOK_PATH
)
