from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os, asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# Глобальное множество для хранения chat_id зарегистрированных пользователей
registered_users = set()

# Обработка команды /start: регистрация пользователя и отправка приветственного сообщения
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    registered_users.add(chat_id)  # Сохраняем пользователя для уведомлений
    keyboard = [[InlineKeyboardButton("Зарегистрироваться на вебинар", callback_data="register")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Нажмите кнопку ниже, чтобы зарегистрироваться на вебинар:",
        reply_markup=reply_markup
    )

# Обработка нажатия кнопки регистрации
async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Отмечаем факт нажатия

    # Создаем кнопку для добавления события в календарь (Google Calendar)
    calendar_keyboard = [[InlineKeyboardButton(
        "Добавить в календарь",
        url="https://calendar.google.com/calendar/r/eventedit?text=Вебинар:+ИИ+и+бинарный+маркетинг&dates=20250412T150000Z/20250412T160000Z&details=Присоединяйтесь+к+нашему+вебинару,+где+мы+рассмотрим+технологии+ИИ+в+бинарном+маркетинге&location=Онлайн"
    )]]
    calendar_markup = InlineKeyboardMarkup(calendar_keyboard)

    await query.message.reply_text(
        "Поздравляем! Вы успешно зарегистрировались на вебинар, который состоится 11.04.2025 в 17:00 (Варшава) / 18:00 (Киев).\n\n"
        "Чтобы не пропустить событие, нажмите кнопку ниже для добавления его в календарь:",
        reply_markup=calendar_markup
    )

    # Отправляем бонусное видео (файл bonus.mp4 должен быть доступен)
    await query.message.reply_video(
        video=InputFile("bonus.mp4"),
        caption="Бонус: как использовать ИИ для анализа договоров"
    )

# Функция-уведомление, которую вызовет планировщик: отправляет сообщение "Внимание! Вебинар начнется через 15 минут!" 
def notify_webinar():
    loop = asyncio.get_event_loop()
    for chat_id in list(registered_users):
        asyncio.run_coroutine_threadsafe(
            app.bot.send_message(chat_id, "Внимание! Вебинар начнется через 15 минут!"),
            loop
        )

# Задаем конкретную дату и время для уведомления.
# Например, уведомление в 17:45 12 апреля 2025 года по киевскому времени.
notification_datetime = datetime(2025, 4, 11, 22, 00)

# Настройка планировщика APScheduler для однократного уведомления
scheduler = BackgroundScheduler(timezone="Europe/Kiev")
scheduler.add_job(notify_webinar, 'date', run_date=notification_datetime)
scheduler.start()

# Получаем токен из переменной окружения и создаем объект бота
token = os.environ.get("BOT_TOKEN")
app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(register_callback, pattern="register"))

# Запускаем бота с использованием длинного опроса (polling)
app.run_polling()
