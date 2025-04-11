from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ТВОЙ ТОКЕН (вшит вручную)
TOKEN = "7602339027:AAFy7JjipaQUJenNfXsRgAAkjVQbLgBiH8w"

# Сформированный webhook URL
WEBHOOK_URL = f"https://telegram-webinar-bot.onrender.com/{TOKEN}"

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(">>> /start от", update.effective_user.id)
    await update.message.reply_text("✅ Бот работает!")

# Создание приложения и добавление хендлера
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Отладочный вывод
print("WEBHOOK:", WEBHOOK_URL)

# Запуск с вебхуком
app.run_webhook(
    listen="0.0.0.0",
    port=8443,
    webhook_url=WEBHOOK_URL
)
