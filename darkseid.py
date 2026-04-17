from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
from typing import Final
import logging
import yfinance as yf
import os
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


# Replace with your bot's API token
darkseid_api=os.getenv("DARKSEID_API_TOKEN")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass your bot's token.
    application = Application.builder().token(darkseid_api).build()

    # on different commands - add handlersyay -S ani-cli
    application.add_handler(CommandHandler("start", start))

    # on non command i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_regular_text))

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

async def handle_regular_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This sends a fixed message back to the user in Telegram
    await update.message.reply_text("I received your message, but I only respond to commands! Use /help for commands")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logging.warning(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    main()


