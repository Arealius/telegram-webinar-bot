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

    calendar_keyboard = [[InlineKeyboardButton("📅 Додати до календаря", url="https://calendar.google.com/calendar/r/eventedit?text=%D0%92%D0%B5%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%3A+%D0%98%D0%98+%D0%B8+%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D0%BD%D1%8B%D0%B9+%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%82%D0%B8%D0%BD%D0%B3&dates=20250412T150000Z/20250412T160000Z&details=%D0%9F%D1%80%D0%B8%D1%81%D0%BE%D0%B4%D0%B8%D0%BD%D0%B5%D0%B9%D1%82%D0%B5%D1%81%D1%8C+%D0%BA+%D0%B2%D0%B5%D0%B1%D0%B8%D0%BD%D0%B0%D1%80%D1%83&location=%D0%9E%D0%BD%D0%BB%D0%B0%D0%B9%D0%BD")]]
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
