import os
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = os.environ.get("8708614062:AAHnYtm9t6yRfMcNby2om2DEmfJwvJdgZnM")
CHANNEL = "@kinobox1111"
CHANNEL_INVITE = "https://t.me/+Sjv2o3ws9U1jY2Uy"
FILMS = {
    "102": "🎬 Fast & Furious 10 (2023)",
    "103": "🎬 John Wick 4 (2023)",
    "105": "🎬 Moonfall (2022) - Моҳ афтод",
    "106": "🎬 Тӯйи Беҳтарин - Комедияи тоҷикӣ",
    "107": "🎬 Филми нав 107",
    "108": "🎬 Филми нав 108",
}

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Live!"

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Салом! Рақами филмро фирист: масалан 102")

async def handle_code(update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    if code in FILMS:
        kb = [[InlineKeyboardButton("📢 Обуна шудан", url=CHANNEL_INVITE)],
              [InlineKeyboardButton("✅ Обуна шудам", callback_data=f"check_{code}")]]
        await update.message.reply_text(f"{FILMS[code]}\n\nБарои дидан ба канал обуна шав!", reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text("❌ Код хато! 102, 103, 105-ро санҷ!")

async def check_sub(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    code = query.data.split("_")[1]
    try:
        member = await context.bot.get_chat_member(CHANNEL, query.from_user.id)
        if member.status in ['member','administrator','creator']:
            await query.message.reply_text(f"✅ {FILMS[code]} - https://t.me/kinobox1111")
        else:
            await query.message.reply_text("❌ Обуна нашудед!")
    except:
        await query.message.reply_text("❌ Хатогӣ - ботро админ кун дар канал!")

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_sub))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))
    application.run_polling()
