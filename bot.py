from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, JobQueue
import random
import asyncio

TOKEN = "ВАШ_BOT_TOKEN"

KEYWORDS = {
    "курение": ["курение", "сигарета", "дым", "никотин", "выкурить"],
    "бросить": ["бросить", "отказаться", "перестать", "не курю", "quit"],
}

ADVICE_LIST = [
    "Дыши глубоко и медленно, когда появляется желание закурить.",
    "Помни, зачем ты решил бросить курить — держи цель перед глазами.",
    "Замени сигарету на полезную привычку: вода, фрукт, прогулка.",
    "Отслеживай свои успехи: каждый день без сигареты — победа!",
    "Если возникает стресс, попробуй дыхательные упражнения или короткую прогулку."
]

REMINDERS = [
    "Напоминание: ты уже продержался без сигареты сегодня, молодец!",
    "Сохрани мотивацию — представь себя здоровым и свободным от никотина!",
    "Каждое «нет» сигарете — это шаг к твоей цели."
]

context_data = {"chats": set()}

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой помощник в отказе от курения. Пиши мне о своих чувствах и желаниях, "
        "и я дам советы, как справиться с тягой к сигарете."
    )

async def smart_reply(update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    response = None

    if any(word in text for word in KEYWORDS["курение"]):
        response = random.choice(ADVICE_LIST)
    elif any(word in text for word in KEYWORDS["бросить"]):
        response = "Отлично, что ты хочешь бросить! Продолжай в том же духе. 💪"

    if not response:
        response = "Я не совсем понял, но я могу дать советы по отказу от курения. Попробуй написать, что тебя тревожит."

    await update.message.reply_text(response)

async def track_chats(update, context: ContextTypes.DEFAULT_TYPE):
    context_data["chats"].add(update.effective_chat.id)
    await smart_reply(update, context)

# Функция для отправки напоминаний
async def send_reminder(context: CallbackContext):
    for chat_id in context_data["chats"]:
        await context.bot.send_message(chat_id, random.choice(REMINDERS))

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_chats))

    # JobQueue для напоминаний каждые 2 часа
    app.job_queue.run_repeating(send_reminder, interval=7200, first=10)

    app.run_polling()

if __name__ == "__main__":
    main()
