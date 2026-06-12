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

from functions import chunk_text, clean_and_convert, get_flag_emoji, is_float

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

session = requests.Session()  # Tcp , Keeps HTTP alive, avoids new ssl handshakes


telegram_token = os.getenv(
    "TELEGRAM_TOKEN"
)  # Telegram bot token var, export TELEGRAM_TOKEN="actual token"

response1 = session.get(
    "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
)
cur_dict = response1.json()


async def show_cur(update: Update, context: ContextTypes.DEFAULT_TYPE):

    reply = ""
    try:
        for i in cur_dict:
            reply += f"{i} - {get_flag_emoji(i)} -{cur_dict.get(i)}\n"
        chunks = chunk_text(reply, limit=3994)
        if update.effective_chat is None:
            return
        for c in chunks:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=c)

    except Exception as e:
        print(e)


async def check_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    elif update.message.text is None:
        return
    user_input = update.message.text.lower().split(" ")
    if len(user_input) < 2:
        await update.message.reply_text("Please input more than 2 currencies")
        return

    date = "latest"
    apiVersion = "v1"
    if not is_float(user_input[0]):
        user_input.insert(0, "1")

    multiplier = clean_and_convert(user_input[0])
    from_currency = user_input[1]
    url_base = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/{apiVersion}/currencies/{from_currency}.json"
    reply_message = ""
    try:
        response = session.get(url_base)
        data = response.json()
        for i in user_input[2:]:
            rate = multiplier * data[from_currency][i]
            reply_message += f"{user_input[0]} {from_currency.upper()}{get_flag_emoji(from_currency)} ≈ {rate:,.2f} {i.upper()}{get_flag_emoji(i)}\n"

        await update.message.reply_text(reply_message)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    application = ApplicationBuilder().token(telegram_token).build()
    show_cur_handler = CommandHandler("show_cur", show_cur)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), check_rate)
    application.add_handler(show_cur_handler)
    application.add_handler(echo_handler)

    application.run_polling()
