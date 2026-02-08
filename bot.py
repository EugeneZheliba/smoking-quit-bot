from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update
import random
import datetime

# Токен вашего бота
TOKEN = "ВАШ_BOT_TOKEN"

# Хранилище для пользователей и прогресса
user_data = {}

# Советы и мотивация
ADVICE_LIST = [
    "Сделай глубокий вдох и выдох — тяга к сигарете пройдет.",
    "Вспомни, зачем ты бросил курить. Ты сильнее привычки!",
    "Замени сигарету на стакан воды или короткую прогулку.",
    "Сфокусируйся на пользе для здоровья: лёгкие чистятся, сердце работает лучше.",
]

REMINDERS = [
    "Напоминание: ты уже держишься без сигареты! Продолжай в том же духе.",
    "Мотивация: представь себя свободным от никотина и здоровым.",
]

# Ключевые слова и их синонимы для «умного» ответа
TRIGGERS = {
    "кур": ["сигар", "затянулся", "курю", "тянет", "дым"],
    "стресс": ["нервничаю", "раздражение", "тревога"],
    "хочу": ["нужно", "не могу", "сильное желание"]
}

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    user_data[user_id] = {"start_time": datetime.datetime.now(), "last_message": ""}
    await update.message.reply_text(
        "Привет! Я твой помощник в отказе от курения.\n"
        "Пиши мне, когда тянет закурить, и я дам советы.\n"
        "Я буду присылать мотивацию и напоминания каждый день."
    )

async def progress(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    if user_id in user_data:
        start_time = user_data[user_id]["start_time"]
        elapsed = datetime.datetime.now() - start_time
        hours = elapsed.total_seconds() // 3600
        days = hours // 24
        await update.message.reply_text(
            f"Ты держишься без сигарет уже {int(days)} дней и {int(hours % 24)} часов! Молодец!"
        )
    else:
        await update.message.reply_text("Ты ещё не начал со мной путь к свободе от курения. Используй /start.")

# Умные ответы по ключевым словам и синонимам
async def smart_reply(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    text = update.message.text.lower()
    response = "Я могу дать советы по отказу от курения, напиши, если тянет закурить."

    for key, synonyms in TRIGGERS.items():
        if any(word in text for word in synonyms):
            response = random.choice(ADVICE_LIST)
            break

    if user_id in user_data:
        user_data[user_id]["last_message"] = text
    else:
        user_data[user_id] = {"start_time": datetime.datetime.now(), "last_message": text}

    await update.message.reply_text(response)

# Функция для регулярных напоминаний
async def send_reminder(context: CallbackContext):
    for user_id in user_data:
        await context.bot.send_message(chat_id=user_id, text=random.choice(REMINDERS))

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("progress", progress))
    # Обработчик всех текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))

    # Напоминания каждые 4 часа
    app.job_queue.run_repeating(send_reminder, interval=14400, first=10)

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
