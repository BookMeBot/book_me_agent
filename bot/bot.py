# Main Telegram bot entry point
from handlers import handle_message, start
from telegram.ext import Update


def main():
    import os

    updater = Update(os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher
    dp = updater.dispatcher
    dp.add_handler(start)
    dp.add_handler(handle_message)
    dp.add_handler(handle_message)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
