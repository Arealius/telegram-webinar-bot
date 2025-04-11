from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

VIDEO_PATH = "bonus.mp4"  # Положи свой видеофайл с таким именем, если надо

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Зареєструватися на вебінар", callback_data="register")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Привіт! Натисни кнопку нижче, щоб зареєструватися:", reply_markup=reply_markup)

async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    calendar_keyboard = [[InlineKeyboardButton("📅 Додати до календаря", url="https://raw.githubusercontent.com/Arealius/telegram-webinar-bot/refs/heads/main/event.ics")]]
    calendar_markup = InlineKeyboardMarkup(calendar_keyboard)

    await query.message.reply_text(
        "🎉 Ви успішно зареєструвалися на вебінар 11.04.2025 о 17:00 (Варшава) / 18:00 (Київ)!\n\n"
        "Щоб не пропустити — додайте до календаря 👇",
        reply_markup=calendar_markup
    )

    await query.message.reply_video(
        video=InputFile(VIDEO_PATH),
        caption="🎁 Подарунок: як використовувати AI для аналізу договорів 📄"
    )

token = os.environ.get("BOT_TOKEN")  # Считываем токен из переменной окружения
app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(register_callback, pattern="register"))

app.run_polling()
