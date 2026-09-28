import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

TOKEN ="8708614062:AAHEnyeNyxX_usaSstLrNlwuld-l2CsaOqY"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Салом! Номи киноро нависед:\nМасалан: Avatar, Wednesday")

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    keyboard = [[InlineKeyboardButton("▶️ Тамошо дар Kinobox", url=f"https://kinobox.to/search?q={query}")]]
    await update.message.reply_text(f"🎬 Ҷустуҷӯ: {query}", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    app.run_polling()

if __name__ == "__main__":
    main()
