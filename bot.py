import logging
import os

import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

session = requests.Session()  # Tcp tunneling?


telegram_token = os.getenv(
    "TELEGRAM_TOKEN"
)  # Telegram bot token var, export TELEGRAM_TOKEN="actual token"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def check_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower().split(" ")
    if len(user_input) != 2:
        await update.message.reply_text("Please input exactly 2 currencies")
        return
    date = "latest"
    apiVersion = "v1"
    from_currency, to_currency = user_input[0], user_input[1]
    url_base = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/{apiVersion}/currencies/{from_currency}.json"
    response = session.get(url_base)
    data = response.json()
    rate = data[from_currency][to_currency]
    await update.message.reply_text(
        f"1 {from_currency.upper()} = {rate:.2f} {to_currency.upper()}"
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(telegram_token).build()
    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), check_rate)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
