import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = "8708614062:AAF0a4nXvEgKDJ4VkKQbq7w0nr52LWMw1Wc"
CHANNEL_INVITE = "https://t.me/+Sjv2o3ws9gdmMjhi"

app = Flask(__name__)
@app.route('/')
def home():
    return "Kino Box @KinoBox111_bot Live!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📢 Обуна шудан", url=CHANNEL_INVITE)],[InlineKeyboardButton("✅ Обуна шудам", callback_data="check_sub")]]
    await update.message.reply_text("👋 Салом! Ба Kino Box хуш омадед 🎬\n\n📢 Обуна шавед:\n"+CHANNEL_INVITE, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("✅ Зӯр ака! 🎉\n\n🎥 Номи киноро нависед:")

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text
    keyboard = [[InlineKeyboardButton(f"▶️ Тамошо - {q}", url=f"https://kinobox.to/search?q={q}")],[InlineKeyboardButton("📢 Канали мо", url=CHANNEL_INVITE)]]
    await update.message.reply_text(f"🎬 {q}\n✅ Ёфт шуд!", reply_markup=InlineKeyboardMarkup(keyboard))

def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_check, pattern="check_sub"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
