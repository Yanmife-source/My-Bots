import yfinance as yf
import pandas as pd
import logging
from datetime import datetime
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
#import /home/oluwayanmife/naeve/ransom/hack
import os
from dotenv import load_dotenv



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Access the bot's API token
load_dotenv()
tatsumi_api=os.getenv("TATSUMI_API_TOKEN")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass your bot's token.
    application = Application.builder().token(tatsumi_api).build()

    # on different commands - add handlersyay -S ani-cli
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("track",track_stocks))

    # on non command i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Register the error handler
    application.add_error_handler(error)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    print("Bot is running...")
    application.run_polling(poll_interval=3)


# Define the command handler functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I am a bot in progress, run the /help command to know the commands",
        reply_markup=None # You can add keyboards here
    )
    global start_bot
    start_bot=True

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Use /start to to start the bot \nUse /help to know the list of commands and how to use the bot\nUse /track to know the stock prices ")
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logging.warning(f'Update {update} caused error {context.error}')

async def track_stocks(update: Update,context: ContextTypes.DEFAULT_TYPE) ->None:
    
    # Fetch current market data
    if start_bot:
        symbols = ["BTC-USD", "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META"]
        await update.message.reply_text("Fetching  stock prices, please wait..")
        try:
            data = yf.download(symbols, period="1d", interval="1m",timeout=10)
            latest_prices = data['Close'].iloc[-1]
            if latest_prices.isna().any():
                raise ValueError
        except ValueError:
            await update.message.reply_text("The stock market is closed at the moment...\nTry again later") 
        else:
            await update.message.reply_text(f"{latest_prices}  ")
    else:
        await update.message.reply_text(f"You might need to start up the bot first using the /start command")



if __name__ == '__main__':
    main()
