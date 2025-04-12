import os
import json
import asyncio
from datetime import datetime, timedelta
from pytz import timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()

# --- Хранилище пользователей ---
registered_users = set()

def load_users():
    global registered_users
    try:
        with open("users.json", "r") as f:
            registered_users = set(json.load(f))
    except FileNotFoundError:
        registered_users = set()

def save_users():
    with open("users.json", "w") as f:
        json.dump(list(registered_users), f)

# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    registered_users.add(chat_id)
    save_users()

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

# --- Обработка кнопки ---
async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

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

# --- Уведомление ---
def notify_webinar():
    loop = asyncio.get_event_loop()
    for chat_id in registered_users:
        asyncio.run_coroutine_threadsafe(
            app.bot.send_message(chat_id, "🔔 Напоминание: вебинар начнется через 15 минут!"),
            loop
        )

# --- Планировщик с учетом Киева ---
scheduler = BackgroundScheduler(timezone="Europe/Kiev")
kiev_time = datetime.now(timezone("Europe/Kiev")) + timedelta(minutes=3)
scheduler.add_job(notify_webinar, 'date', run_date=kiev_time)
scheduler.start()

# --- Запуск бота ---
TOKEN = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(TOKEN).build()

load_users()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(register_callback, pattern="register"))

print("🔁 Бот запущен в режиме polling...")
app.run_polling()
