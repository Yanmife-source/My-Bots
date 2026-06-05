from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes,CallbackQueryHandler,ConversationHandler
from scraper_agent import search_product
from typing import Final
import logging
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
WAITING_FOR_PRODUCT = 1

def main() -> None:
    """Start the bot."""
    # Create the Application and pass your bot's token.
    application = (
        Application.builder()
       .token(darkseid_api)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .pool_timeout(30.0)
        .build()

    )

    conv_handler=ConversationHandler(
        entry_points=[CallbackQueryHandler(button_click)],
        states={
            WAITING_FOR_PRODUCT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search)  # waits for text
            ]
        },
        per_message=False,
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # on different commands - add handlersyay -S ani-cli
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    # on non command i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_regular_text))

    # Register the error handler
    application.add_error_handler(error)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    print("Bot is running...")
    application.run_polling(poll_interval=2)



# Define the command handler functionsq
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
     # Build your button matrix layout
    keyboard = [
    [InlineKeyboardButton("Search Product", callback_data="search")]
    ]    

    # 2. Wrap it
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_html(
        f"Hi {user.mention_html()}! Welcome to Tudor Price Bot 👋\nFind the cheapest prices across Jumia, Konga and Jiji.",
         reply_markup=reply_markup
         )

async def handle_regular_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This sends a fixed message back to the user in Telegram
    await update.message.reply_text("I received your message, but I only respond to commands! Use /help for commands")

async def button_click(update, context):
    query = update.callback_query
    await query.answer()  # stops the loading spinner

    if query.data == "search":
        await query.edit_message_text("🔍 What product are you looking for?")
        return WAITING_FOR_PRODUCT  # tells ConversationHandler to wait for user input

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logging.warning(f'Update {update} caused error {context.error}')

async def handle_search(update, context):
    product = update.message.text
    loading_msg = await update.message.reply_text("⏳ Scraping Jumia, Konga and Jiji...")
    result = await search_product(product)
    await loading_msg.edit_text(result)

async def cancel(update: Update, context):
    await update.message.reply_text("Search cancelled due to unprecedented issues.")
    return ConversationHandler.END



if __name__ == '__main__':
    main()


