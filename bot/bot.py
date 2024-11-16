# Main Telegram bot entry point
import os
from handlers import handle_message, start
from telegram.ext import Application, CommandHandler, MessageHandler, filters


def main():

    # Initialize the application
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()



if __name__ == "__main__":
    main()
