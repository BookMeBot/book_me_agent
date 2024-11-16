import requests

BASE_URL = "http://localhost:8000"

def handle_user_message(user_message):
    """
    Processes the user message and routes it through the appropriate API endpoints.
    """
    try:
        # Step 1: Parse intent
        response = requests.post(f"{BASE_URL}/intent/", json={"message": user_message})
        if response.status_code != 200:
            print("Error: Could not parse intent.")
            return

        result = response.json()
        intent = result["intent"]
        data = result["data"]
        next_step = result["next_step"]

        print(f"Intent: {intent}")
        print(f"Next Step: {next_step}")

        # Step 2: Perform next step based on the intent and next_step
        if next_step == "/search/":
            search_response = requests.post(f"{BASE_URL}{next_step}", json=data)
            if search_response.status_code == 200:
                print(f"Search Results: {search_response.json()}")
            else:
                print(f"Error: {search_response.text}")
        elif next_step == "/qa/":
            qa_response = requests.post(f"{BASE_URL}{next_step}", json=data)
            if qa_response.status_code == 200:
                print(f"Answer: {qa_response.json()}")
            else:
                print(f"Error: {qa_response.text}")
        elif next_step == "/booking/":
            booking_response = requests.post(f"{BASE_URL}{next_step}", json=data)
            if booking_response.status_code == 200:
                print(f"Booking Confirmation: {booking_response.json()}")
            else:
                print(f"Error: {booking_response.text}")
        else:
            print("Unhandled next step. Please check your message or try again.")
    except Exception as e:
        print(f"Error handling user message: {e}")

def main():
    """
    Command-line interface for interacting with the API.
    """
    print("Welcome to the BookMeBot CLI! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Process the user's message through the API
        handle_user_message(user_input)

if __name__ == "__main__":
    main()


# # # Main Telegram bot entry point
# # from handlers import handle_message, start
# # from telegram.ext import Updater


# # def main():
# #     import os

# #     updater = Updater(os.getenv("TELEGRAM_BOT_TOKEN"))
# #     dp = updater.dispatcher
# #     dp.add_handler(start)
# #     dp.add_handler(handle_message)
# #     updater.start_polling()
# #     updater.idle()


# # if __name__ == "__main__":
# #     main()

# import os
# from agents.intent_parser import parse_intent

# def main():
#     print("Welcome to the command-line bot! Type 'exit' to quit.")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == 'exit':
#             print("Goodbye!")
#             break

#         # Parse the user's intent
#         intent, data = parse_intent(user_input)

#         if intent:
#             print(f"Intent: {intent}\nData: {data}")
#         else:
#             print("I'm not sure what you mean. Could you provide more details?")

# if __name__ == "__main__":
#     main()
