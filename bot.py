from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext
)
import random
import datetime

TOKEN = "8347663636:AAEXmoHDtxn98dgu13KeQLQzSW33SzpXn4c"

# Словарь подсказок для отказа от курения
RESPONSES = {
    "курить": [
        "Попробуй сделать глубокий вдох и выпить воды вместо сигареты.",
        "Отвлекись на прогулку, это помогает снизить желание курить.",
        "Вспомни, почему ты решил бросить курить — это мотивирует."
    ],
    "сигарета": [
        "Сигарета ничего хорошего не даст, а твой прогресс важнее!",
        "Давай заменим сигарету на полезную привычку — воду или фрукты."
    ],
    "никотин": [
        "Никотин — временное удовольствие, а твое здоровье — навсегда!",
        "Старайся переждать желание, оно проходит за несколько минут."
    ],
    "тянуться": [
        "Попробуй заменить привычку тянуться к сигарете на дыхательное упражнение.",
        "Каждое желание — шанс стать сильнее."
    ]
}

# Хранение прогресса пользователей
user_progress = {}

# Команды
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_progress[user.id] = datetime.datetime.now()
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я помогу тебе бросить курить. "
        "Пиши свои ощущения, и я дам советы."
    )

async def progress(update: Update, context: CallbackContext):
    user = update.effective_user
    start_time = user_progress.get(user.id)
    if start_time:
        days = (datetime.datetime.now() - start_time).days
        await update.message.reply_text(f"Ты не куришь уже {days} дней! Молодец!")
    else:
        await update.message.reply_text("Ты ещё не начал отслеживать прогресс. Напиши /start.")

# "Умные" ответы по синонимам
async def smart_reply(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    for key, answers in RESPONSES.items():
        if key in text:
            await update.message.reply_text(random.choice(answers))
            return
    # Ответ по умолчанию, если не найдено ключевое слово
    await update.message.reply_text("Держись, каждый момент без сигареты — победа!")

# Напоминания каждые 2 часа
async def send_reminder(context: CallbackContext):
    for user_id in user_progress:
        await context.bot.send_message(
            chat_id=user_id,
            text="Напоминание: дыши глубоко, пей воду и не кури! 💪"
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("progress", progress))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))

    # JobQueue
    app.job_queue.run_repeating(send_reminder, interval=7200, first=10)  # каждые 2 часа

    app.run_polling()

if __name__ == "__main__":
    main()
