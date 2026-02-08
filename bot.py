from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random

# ====== Мотивационные сообщения ======
motivations = [
    "Отлично! Каждый день без сигареты — победа.",
    "Помни, чем дольше ты держишься, тем сильнее твоя сила воли!",
    "Ты справляешься, продолжай так!",
    "Отказ от курения — инвестиция в здоровье."
]

# ====== Ответы на сигналы собеседника ======
keywords = {
    "тянет": ["Держись! Сделай глубокий вдох и выпей воды."],
    "хочу курить": ["Попробуй отвлечься: прогуляйся или сделай дыхательное упражнение."],
    "стресс": ["Стресс пройдёт! Попробуй медитацию или короткую прогулку."],
    "нерв": ["Считай до 10, глубоко вдохни и выдохни. Всё под контролем."],
}

# ====== Обработчики команд ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-помощник в отказе от курения.\n"
        "Команды:\n"
        "/mood - поделиться настроением\n"
        "/help - подсказки и мотивация\n\n"
        "Просто пиши мне свои ощущения или трудности — я дам советы!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Если тебя тянет курить, напиши об этом, и я дам совет.\n"
        "Также можешь использовать /mood, чтобы записать своё настроение.\n"
        "Я буду напоминать о мотивации и поддерживать тебя каждый день!"
    )

# ====== Логирование настроения ======
async def log_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        mood_text = " ".join(context.args)
        await update.message.reply_text(
            f"Настроение записано: {mood_text}\n"
            f"{random.choice(motivations)}"
        )
    else:
        await update.message.reply_text("Пиши после команды, как у тебя настроение. Например: /mood Отличное")

# ====== Обработка любых сообщений ======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    responded = False
    for key, responses in keywords.items():
        if key in text:
            await update.message.reply_text(random.choice(responses))
            responded = True
            break
    if not responded:
        await update.message.reply_text(random.choice(motivations))

# ====== Основная функция ======
def main():
    app = ApplicationBuilder().token("8347663636:AAEXmoHDtxn98dgu13KeQLQzSW33SzpXn4c").build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("mood", log_mood))

    # Сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск
    app.run_polling()

if __name__ == "__main__":
    main()
