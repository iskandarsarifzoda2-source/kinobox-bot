import os
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import threading

# Токен - агар дар Render BOT_TOKEN гузошта бошӣ, ҳамон кор мекунад
TOKEN = os.environ.get("BOT_TOKEN", "8209313898:AAF9aNSR9wZ9yd4v0QpD0Uo0fO4qB5J0ZgM")
CHANNEL = "@kinobox1111"
CHANNEL_INVITE = "https://t.me/+Sjv2o3ws9gdmMjhi"

# 👇 ИН ҶО ФИЛМҲОРО ИЛОВА КУН! Ҳар вақт метавонӣ зиёд кунӣ!
FILMS = {
    "102": "🎬 Fast & Furious 10 (2023)",
    "103": "🎬 John Wick 4 (2023)",
    "105": "🎬 Moonfall (2022) - Моҳ афтод",
    "106": "🎬 Тӯйи Беҳтарин - Комедияи тоҷикӣ",
    "107": "🎬 Филми нав - номашро инҷо нависед",
    "108": "🎬 Филми нав 108",
}

app = Flask(__name__)
@app.route('/')
def home():
    return "Kino Box @KinoBox111_bot Live! ✅"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Обуна шудан", url=CHANNEL_INVITE)],
        [InlineKeyboardButton("✅ Обуна шудам", callback_data="check_sub")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Салом! Ба Kino Box хуш омадед!\n\n"
        "📢 Барои гирифтани филм ба канали мо обуна шавед!\n\n"
        "🔢 Баъд коди филмро нависед:\n"
        "Масалан: 102, 105, 106",
        reply_markup=reply_markup
    )

async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            await query.edit_message_text("✅ Ташаккур! Обуна шудед!\n\n🔢 Ҳозир коди филмро нависед: 105, 106...")
        else:
            await query.answer("❌ Шумо ҳоло обуна нашудед! Аввал Обуна шавед!", show_alert=True)
    except:
        await query.edit_message_text("✅ Обуна қабул шуд! Коди филмро нависед: 105, 106...")

async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or update.message.caption or ""
    code = text.strip().split()[0] if text else ""
    code = ''.join(filter(str.isdigit, code)) # фақат рақам

    if not code:
        await update.message.reply_text("❌ Лутфан танҳо рақами коди филмро нависед: масалан 105")
        return

    film_name = FILMS.get(code, f"🎬 Филм бо коди {code} - Ба наздикӣ номаш илова мешавад")

    # Инҷо ту метавонӣ линки филмро равон кунӣ
    await update.message.reply_text(
        f"✅ Сабт шуд! Коди {code}\n\n"
        f"{film_name}\n\n"
        f"📥 Барои гирифтани линк ба {CHANNEL} нависед ё интизор шавед!\n\n"
        f"💡 Админ ба зудӣ филмро мефиристад!"
    )

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(check_sub, pattern="check_sub"))
    application.add_handler(MessageHandler(filters.TEXT | filters.VIDEO | filters.PHOTO | filters.Document.ALL, handle_code))
    application.run_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
