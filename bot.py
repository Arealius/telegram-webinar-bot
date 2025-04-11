import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

# Глобальное множество для хранения chat_id пользователей
registered_users = set()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    registered_users.add(chat_id)

    keyboard = [
        [InlineKeyboardButton("Зарегистрироваться на вебинар", callback_data="register")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! Нажми кнопку для регистрации на вебинар:",
        reply_markup=reply_markup
    )

# Обработка кнопки
async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✅ Вы успешно зарегистрировались на вебинар!")

# Уведомление перед вебинаром
def notify_webinar():
    loop = asyncio.get_event_loop()
    for chat_id in list(registered_users):
        asyncio.run_coroutine_threadsafe(
            app.bot.send_message(chat_id, "⏰ Напоминание: вебинар начнется через 15 минут!"),
            loop
        )

# Планировщик (каждый день в 17:45 по Киеву)
scheduler = BackgroundScheduler(timezone="Europe/Kiev")
scheduler.add_job(notify_webinar, 'cron', hour=17, minute=45)
scheduler.start()

# Создание бота
token = os.environ.get("BOT_TOKEN")
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(register_callback, pattern="register"))

# Webhook-подключение для Render
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_URL = f"https://{WEBHOOK_HOST}/{token}"

app.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 8443)),
    webhook_url=WEBHOOK_URL
)
