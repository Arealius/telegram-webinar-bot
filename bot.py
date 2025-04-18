import os
import json
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()

# 📁 JSON-файл хранения
USERS_FILE = "registered_users.json"

# 📥 Загрузка зарегистрированных пользователей
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return set(json.load(f))
    return set()

# 💾 Сохранение пользователей
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)

registered_users = load_users()

# 🕒 Планировщик
scheduler = BackgroundScheduler(timezone="Europe/Kiev")
scheduler.start()

# 📲 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    registered_users.add(chat_id)
    save_users(registered_users)

    keyboard = [[InlineKeyboardButton("Зарегистрироваться на вебинар", callback_data="register")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! 👋\n"
        "На вебинаре «Автоматизируй рутину с ИИ» я покажу, как использовать искусственный интеллект для автоматизации процессов и личных задач.\n\n"
        "Вебинар пройдёт сегодня:\n"
        "12.04.2025 в 17:00 Варшава | 18:00 Киев.\n\n"
        "Никакой лишней теории — только практические инструменты, которые уже сегодня помогут сэкономить время и ресурсы. Вы узнаете:\n\n"
        "✅ Как автоматизировать рутинные задачи без программирования\n"
        "✅ Какие ИИ-инструменты помогут в работе и жизни\n"
        "✅ Реальные кейсы, которые я ежедневно использую в своих компаниях\n\n"
        "Нажмите «Зарегистрироваться» и получите подарок 🎁 — 30-минутный бесплатный урок:\n"
        "«Как автоматизировать работу юриста и обработку документов с помощью ИИ».",
        reply_markup=reply_markup
    )

# 📥 Обработка кнопки регистрации
async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.from_user.id
    registered_users.add(chat_id)
    save_users(registered_users)

    # Устанавливаем дату вебинара (замени при необходимости)
    webinar_time = datetime(2025, 4, 12, 18, 0)  # Киев 18:00

    # 🕔 Напоминание за 5 минут
    scheduler.add_job(
        lambda: asyncio.run_coroutine_threadsafe(
            app.bot.send_message(chat_id, "🔔 Напоминание: вебинар начнется через 5 минут!"),
            asyncio.get_event_loop()
        ),
        'date',
        run_date=webinar_time - timedelta(minutes=5)
    )

    # 🕐 Напоминание за 1 минуту
    scheduler.add_job(
        lambda: asyncio.run_coroutine_threadsafe(
            app.bot.send_message(chat_id, "⏰ Вебинар начинается через 1 минуту! Заходите!"),
            asyncio.get_event_loop()
        ),
        'date',
        run_date=webinar_time - timedelta(minutes=1)
    )

    calendar_keyboard = [[InlineKeyboardButton(
        "Добавить в календарь",
        url="https://calendar.google.com/calendar/r/eventedit?text=Вебинар:+ИИ+и+бинарный+маркетинг&dates=20250412T150000Z/20250412T160000Z&details=Присоединяйтесь+к+нашему+вебинару,+где+мы+рассмотрим+технологии+ИИ+в+бинарном+маркетинге&location=Онлайн"
    )]]
    calendar_markup = InlineKeyboardMarkup(calendar_keyboard)

    await query.message.reply_text(
        "Поздравляем! Вы зарегистрированы на вебинар, который состоится 12.04.2025 в 17:00 (Варшава) / 18:00 (Киев).\n\n"
        "Нажмите кнопку ниже, чтобы добавить его в календарь:",
        reply_markup=calendar_markup
    )

    await query.message.reply_video(
        video="https://infinitysync.net/images/bonus.mp4",
        caption="🎁 Бонус: как использовать ИИ для анализа договоров"
    )

# 🚀 Запуск бота
TOKEN = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(register_callback, pattern="register"))

print("🔁 Бот запущен. Уведомления будут отправлены за 5 и 1 минуту до вебинара.")
app.run_polling()
