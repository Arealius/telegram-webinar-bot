from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔑 Укажи сюда свой токен
TOKEN = "7602339027:AAFy7JjipaQUJenNfXsRgAAkjVQbLgBiH8w"

# 🌐 Webhook URL
WEBHOOK_URL = f"https://telegram-webinar-bot.onrender.com/{TOKEN}"

# ✅ Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(">>> /start от", update.effective_user.id)
    await update.message.reply_text("✅ Бот работает!")

# 🚀 Приложение Telegram
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# 🌍 Запуск через Webhook
app.run_webhook(
    listen="0.0.0.0",
    port=8443,
    webhook_url=WEBHOOK_URL,
    webhook_path=f"/{TOKEN}"  # ВАЖНО: Telegram обращается к этому пути
)
