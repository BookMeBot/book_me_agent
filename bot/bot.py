# # Main Telegram bot entry point
# from handlers import handle_message, start
# from telegram.ext import Updater


# def main():
#     import os

#     updater = Updater(os.getenv("TELEGRAM_BOT_TOKEN"))
#     dp = updater.dispatcher
#     dp.add_handler(start)
#     dp.add_handler(handle_message)
#     updater.start_polling()
#     updater.idle()


# if __name__ == "__main__":
#     main()

import os
from agents.intent_parser import parse_intent

def main():
    print("Welcome to the command-line bot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Parse the user's intent
        intent, data = parse_intent(user_input)

        if intent:
            print(f"Intent: {intent}\nData: {data}")
        else:
            print("I'm not sure what you mean. Could you provide more details?")

if __name__ == "__main__":
    main()
