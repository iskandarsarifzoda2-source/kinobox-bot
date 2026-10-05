import os
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN", "8708614062:AAEZMLewIKsndI2JaB531OCXFi1Zo8sGLSM")
CHANNEL = "@kinobox1111"
CHANNEL_INVITE = "https://t.me/+Sjv2o3ws9yM1NjEy"

FILMS = {
    "102": "🎬 Fast & Furious 10 (2023)",
    "103": "🎬 John Wick 4 (2023)",
    "105": "🎬 Moonfall (2022) - Моҳ афтод",
    "106": "🎬 Тӯйи Беҳтарин - Комедияи тоҷикӣ",
    "107": "🎬 Филми нав - номашро инҷо илова кун",
    "108": "🎬 Филми нав 108",
}

app = Flask(__name__)
@app.route('/')
def home(): return "KinoBox Bot Live!"

async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)
        if member.status in ['member','administrator','creator']: return True
    except: pass
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_sub(update, context):
        btn = [[InlineKeyboardButton("📢 Обуна шудан", url=CHANNEL_INVITE)],
               [InlineKeyboardButton("✅ Санҷиш", callback_data="check")]]
        await update.message.reply_text("Барои истифода аввал ба канал обуна шав! 👇", reply_markup=InlineKeyboardMarkup(btn))
        return
    await update.message.reply_text("Салом! 🎬 Коди филмро фирист, масалан: 102")

async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_sub(update, context):
        await start(update, context); return
    code = update.message.text.strip()
    film = FILMS.get(code)
    if film:
        await update.message.reply_text(f"{film}\n\nЛинк: Дар канал @kinobox1111 ҷустуҷӯ кун 😉")
    else:
        await update.message.reply_text("Код нодуруст! 😕 Коди дуруст фирист, масалан 102")

async def check_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    if await check_sub(update, context):
        await q.edit_message_text("Офарин! ✅ Обуна шудӣ! Коди филмро фирист.")
    else:
        await q.answer("Ҳанӯз обуна нашудаӣ! 😕", show_alert=True)

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))
    from telegram.ext import CallbackQueryHandler
    application.add_handler(CallbackQueryHandler(check_btn))
    application.run_polling()

threading.Thread(target=run_bot, daemon=True).start()
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
