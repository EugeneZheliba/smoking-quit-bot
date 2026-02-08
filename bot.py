import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

TOKEN = os.getenv("BOT_TOKEN")  # <- токен не вставляем вручную!

ADVICE_LIST = [
    "Начни с малого: откладывай первую сигарету дня на 30 минут.",
    "Пей воду, когда хочется курить — тяга часто проходит через 5–10 минут.",
    "Избегай триггеров: кофе, алкоголь, стресс в первые недели.",
    "Напоминай себе, зачем ты бросаешь: здоровье, деньги, свобода.",
    "Каждый день без сигарет — это уже победа."
]

CRAVING_HELP = [
    "Тяга длится не больше 10 минут. Сделай 10 глубоких вдохов.",
    "Отвлекись: пройдися, умойся холодной водой.",
    "Ты не хочешь сигарету — ты хочешь, чтобы прошло напряжение. Оно пройдёт.",
    "Вспомни: ты уже принял решение бросить. Не сдавайся сейчас.",
    "Каждый раз, когда ты не куришь — зависимость слабеет."
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋\nЯ помогу тебе бросить курить 🚭\n\nКоманды:\n/advice\n/craving\n/money <цена_пачки> <пачек_в_день> <дней>"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚭 Помощь по боту\n\n"
        "/start — запуск бота\n"
        "/advice — совет для отказа от курения\n"
        "/craving — поддержка при тяге\n"
        "/money — расчёт сэкономленных денег\n\nПример: /money 90 1 30"
    )

async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(ADVICE_LIST))

async def craving(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(CRAVING_HELP))

async def money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = float(context.args[0])
        packs_per_day = float(context.args[1])
        days = int(context.args[2])
        total = price * packs_per_day * days
        await update.message.reply_text(f"💰 Экономия за {days} дней: {total:.2f} грн")
    except:
        await update.message.reply_text("Использование:\n/money <цена_пачки> <пачек_в_день> <дней>\nПример: /money 90 1 30")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("advice", advice))
    app.add_handler(CommandHandler("craving", craving))
    app.add_handler(CommandHandler("money", money))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
