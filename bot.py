from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler

# Глобальное множество для хранения chat_id пользователей, зарегистрированных на вебинар
registered_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Сохраняем chat_id пользователя при регистрации
    chat_id = update.message.chat.id
    registered_users.add(chat_id)
    
    keyboard = [
        [InlineKeyboardButton("Зарегистрироваться на вебинар", callback_data="register")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми кнопку для регистрации на вебинар:", reply_markup=reply_markup)

async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Можно отправить подтверждение регистрации и бонусное сообщение
    await query.message.reply_text("Вы успешно зарегистрировались на вебинар!")
    # Дополнительно можно отправить бонусное видео, если нужно:
    # await query.message.reply_video(video=InputFile("bonus.mp4"), caption="Подарок: бонусное видео")

def notify_webinar():
    """
    Функция уведомления. Она вызывается планировщиком APScheduler.
    Для каждого зарегистрированного пользователя отправляется сообщение.
    """
    loop = asyncio.get_event_loop()
    for chat_id in list(registered_users):
        # Отправляем уведомление асинхронно в основном event loop
        asyncio.run_coroutine_threadsafe(
            app.bot.send_message(chat_id, "Внимание: вебинар начнется через 15 минут!"), loop
        )

# Настройка APScheduler для отправки уведомления в нужное время.
# В этом примере предполагается, что вебинар начинается каждый день в 18:00 по киевскому времени.
# Тогда уведомление будет отправлено в 17:45 (т.е. за 15 минут до вебинара).
scheduler = BackgroundScheduler(timezone="Europe/Kiev")
scheduler.add_job(notify_webinar, 'cron', hour=23, minute=15)
scheduler.start()

# Создание и запуск бота
token = os.environ.get("BOT_TOKEN")
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(register_callback, pattern="register"))

app.run_polling()
