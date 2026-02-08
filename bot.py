from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta, time as dt_time
import random
import asyncio

# ======= Пользователи =======
# Для простоты — словарь в памяти
users = {}  # user_id : {"mood": [], "cravings": [], "challenges_done": []}

# ======= Списки мотиваций и заданий =======
MOTIVATION_MESSAGES = [
    "Каждый день без сигареты — шаг к свободе!",
    "Ты справляешься! Сделай глубокий вдох и почувствуй силу!",
    "Сила воли растёт каждый день, продолжай так!",
    "Не сдавайся! Маленькая победа сегодня — большая завтра."
]

MINI_CHALLENGES = [
    "Сделай 10 приседаний",
    "Выпей стакан воды",
    "Сделай 5 глубоких вдохов и выдохов",
    "Запиши 3 вещи, за которые благодарен"
]

# ======= Хендлеры команд =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = {"mood": [], "cravings": [], "challenges_done": []}
    await update.message.reply_text(
        "Привет! Я твой помощник по отказу от курения.\n"
        "Я буду напоминать тебе о дыхательных упражнениях, мотивации и мини-заданиях.\n"
        "Пиши 'тягa' если появляется желание курить, или 'настроение' чтобы сообщить как ты себя чувствуешь."
    )

async def log_craving(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.setdefault(user_id, {"mood": [], "cravings": [], "challenges_done": []})
    users[user_id]["cravings"].append((datetime.now(), True))
    await update.message.reply_text(
        "Записал твою тягу к курению. Давай сделаем маленькое отвлечение!"
    )
    # Авто-задание для отвлечения
    challenge = random.choice(MINI_CHALLENGES)
    await update.message.reply_text(f"Попробуй сделать это: {challenge}")

async def log_mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mood_text = ' '.join(context.args).lower()
    users.setdefault(user_id, {"mood": [], "cravings": [], "challenges_done": []})
    if "хорошо" in mood_text or "отлично" in mood_text:
        mood = "mood_good"
    elif "плохо" in mood_text or "устал" in mood_text:
        mood = "mood_bad"
    else:
        mood = "mood_neutral"
    users[user_id]["mood"].append((datetime.now(), mood))
    await update.message.reply_text("Отлично, записал твоё настроение!")

# ======= Авто-нагадування =======
async def auto_check(context: ContextTypes.DEFAULT_TYPE):
    for user_id, data in users.items():
        last_mood = data["mood"][-1][1] if data["mood"] else None
        if last_mood == "mood_bad":
            msg = "Вижу, что последние дни были тяжёлые. Сделай дыхательное упражнение или короткую прогулку!"
        elif last_mood == "mood_good":
            msg = "Отлично! Продолжай держать себя в форме — каждый день без сигарет важен!"
        else:
            msg = random.choice([
                "Как твоё настроение сейчас? 😊",
                "Проверка: была ли тяга к курению сегодня?",
                "Не забывай пить воду и делать дыхательные упражнения!"
            ])
        await context.bot.send_message(chat_id=user_id, text=msg)

# ======= Ответ на любое сообщение =======
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    if "тягa" in user_text or "хочу курить" in user_text:
        await log_craving(update, context)
    elif "настроение" in user_text or "как дела" in user_text:
        await update.message.reply_text("Расскажи, как ты себя чувствуешь (хорошо/плохо/нейтрально)")
    else:
        await update.message.reply_text(random.choice(MOTIVATION_MESSAGES))

# ======= Настройка бота и JobQueue =======
def main():
    TOKEN = "8347663636:AAEXmoHDtxn98dgu13KeQLQzSW33SzpXn4c"
    app = ApplicationBuilder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("настроение", log_mood))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Авто-напоминания
    app.job_queue.run_daily(auto_check, time=dt_time(hour=9, minute=0))
    app.job_queue.run_daily(auto_check, time=dt_time(hour=21, minute=0))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
