from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8142653184:AAF5FqVCVR6c1vKaPgZaQ2e2eCoZ-4yVIEs'

# Упражнения по уровню
exercises = [
    "1️⃣ Сделай 5 медленных вдохов. На вдох — 4 секунды, на выдох — 6. Это поможет замедлить пульс.",
    "2️⃣ Найди глазами 5 предметов вокруг. Назови их. Это вернёт тебе ощущение контроля.",
    "3️⃣ Приложи руки к груди и слегка надави — это помогает вернуть тело в 'здесь и сейчас'.",
    "⚠️ Если ничего не помогает — напиши близкому или психологу. Ты не один(а)."
]

# Храним, на каком уровне упражнений человек
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_states[chat_id] = 0
    await send_exercise(update, context)

async def send_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    level = user_states.get(chat_id, 0)

    if level < len(exercises):
        text = exercises[level]
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Помогло", callback_data='helped')],
            [InlineKeyboardButton("❌ Не помогло", callback_data='not_helped')]
        ])
        await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
    else:
        await context.bot.send_message(chat_id=chat_id, text="Это уже всё, что я могу предложить. Может, стоит поговорить с профессионалом.")

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat.id
    await query.answer()

    if query.data == 'helped':
        await context.bot.send_message(chat_id=chat_id, text="Рад, что помогло. Ты справишься. Я рядом, если что ❤️")
        user_states[chat_id] = 0
    else:
        user_states[chat_id] += 1
        await send_exercise(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("panic", start))
    app.add_handler(CallbackQueryHandler(handle_response))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
