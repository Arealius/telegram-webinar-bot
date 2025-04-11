from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔑 Твой токен
TOKEN = "7602339027:AAFy7JjipaQUJenNfXsRgAAkjVQbLgBiH8w"

# 🌐 Webhook URL
WEBHOOK_URL = f"https://telegram-webinar-bot.onrender.com"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(">>> /start от", update.effective_user.id)
    await update.message.reply_text("✅ Бот работает!")

# Запуск приложения
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Запуск с вебхуком
app.run_webhook(
    listen="0.0.0.0",
    port=8443,
    webhook_url=WEBHOOK_URL
)
