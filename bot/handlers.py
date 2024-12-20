# import os
# import sys
# from telegram import __version__ as tg_version
# from telegram.ext import CallbackContext, ConversationHandler, Updater, CommandHandler, MessageHandler, filters 
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from agents.intent_parser import parse_intent
# from agents.search_agent import search_hotels
# from agents.qa_agent import answer_question
# from cdp_agentkit_core.actions.register_basename import register_basename

# #Define states
# CREATE_WALLET, ASSIGN_ENS, TRAVEL_PLANS = range(3)

# user_data = {}

# def start(update: Updater, context: CallbackContext) -> int:
#     chat_id = update.message.chat_id

#     # Create a new wallet for the user using CdpAgentkitWrapper
#     agentkit = CdpAgentkitWrapper()
#     user_wallet = agentkit.export_wallet()
#     user_data[chat_id] = {'wallet': user_wallet}

#     update.message.reply_text(
#         f"Welcome! A new wallet has been created for you. Your wallet address is {user_wallet['default_address_id']}.\n"
#         "Please provide a unique ENS domain name for your agent:"
#     )
#     return ASSIGN_ENS

# def assign_ens(update: Updater, context: CallbackContext) -> int:
#     chat_id = update.message.chat_id
#     ens_name = update.message.text.strip()
#     user_wallet = user_data[chat_id]['wallet']

#     try:
#         # Register the ENS domain
#         register_basename(user_wallet, ens_name)
#         user_data[chat_id]['ens_domain'] = ens_name
#         update.message.reply_text(
#             f"ENS domain '{ens_name}' has been assigned to your wallet.\n"
#             "You can now proceed with your travel plans. Where would you like to go?"
#         )
#         return TRAVEL_PLANS
#     except Exception as e:
#         update.message.reply_text(
#             f"An error occurred while registering the ENS domain: {e}\n"
#             "Please provide a different ENS domain name:"
#         )
#         return ASSIGN_ENS

# def handle_travel_plans(update: Updater, context: CallbackContext) -> int:
#     chat_id = update.message.chat_id
#     user_message = update.message.text

#     parsed_intent = parse_intent(user_message)
#     if not parsed_intent:
#         update.message.reply_text("Sorry, that's an invalid response. Please provide more details.")
#         return TRAVEL_PLANS

#     hotel_options = search_hotels(parsed_intent)
#     if hotel_options:
#         options_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(hotel_options)])
#         update.message.reply_text(f"Here are some options:\n{options_text}")
#     else:
#         update.message.reply_text("No hotel options found matching your criteria.")

#     return ConversationHandler.END

# def handle_message(update: Updater, context: CallbackContext) -> None:
#     chat_id = update.message.chat_id
#     user_message = update.message.text

#     # Parse the user's intent
#     intent, data = parse_intent(user_message)

#     if intent:
#         # Respond based on the parsed intent
#         update.message.reply_text(f"Intent: {intent}\nData: {data}")
#     else:
#         # If no intent is found, ask for more information
#         update.message.reply_text("I'm not sure what you mean. Could you provide more details?")

# def main():
#     TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
#     updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
#     dispatcher = updater.dispatcher

#     # Define the conversation handler
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],
#         states={
#             ASSIGN_ENS: [MessageHandler(filters.TEXT & ~filters.COMMAND, assign_ens)],
#             TRAVEL_PLANS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_travel_plans)],
#         },
#         fallbacks=[],
#     )

#     dispatcher.add_handler(conv_handler)

#     updater.start_polling()
#     updater.idle()


# if __name__ == '__main__':
#     main()

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.intent_parser import parse_intent
from agents.search_agent import search_hotels
from cdp_agentkit_core.actions.register_basename import register_basename

# Define states
CREATE_WALLET, ASSIGN_ENS, TRAVEL_PLANS = range(3)

user_data = {}

def start():
    print("Welcome! A new wallet has been created for you.")
    agentkit = CdpAgentkitWrapper()
    user_wallet = agentkit.export_wallet()
    user_data['wallet'] = user_wallet
    print(f"Your wallet address is {user_wallet['default_address_id']}.")
    print("Please provide a unique ENS domain name for your agent:")
    return ASSIGN_ENS


def handle_message(user_message):
    """
    Process the user's message and respond based on the parsed intent.
    """
    # Parse the user's intent
    intent, data = parse_intent(user_message)

    if intent:
        # Respond based on the parsed intent
        print(f"Intent: {intent}\nData: {data}")
    else:
        # If no intent is found, ask for more information
        print("I'm not sure what you mean. Could you provide more details?")

def assign_ens():
    ens_name = input("ENS Domain: ").strip()
    user_wallet = user_data['wallet']

    try:
        register_basename(user_wallet, ens_name)
        user_data['ens_domain'] = ens_name
        print(f"ENS domain '{ens_name}' has been assigned to your wallet.")
        print("You can now proceed with your travel plans. Where would you like to go?")
        return TRAVEL_PLANS
    except Exception as e:
        print(f"An error occurred while registering the ENS domain: {e}")
        print("Please provide a different ENS domain name:")
        return ASSIGN_ENS

def handle_travel_plans():
    user_message = input("Travel Plans: ")

    parsed_intent = parse_intent(user_message)
    if not parsed_intent:
        print("Sorry, that's an invalid response. Please provide more details.")
        return TRAVEL_PLANS

    hotel_options = search_hotels(parsed_intent)
    if hotel_options:
        options_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(hotel_options)])
        print(f"Here are some options:\n{options_text}")
    else:
        print("No hotel options found matching your criteria.")

    return None  # End the conversation


def handle_user_message(user_message):
    """
    Processes the user message and routes it through the appropriate API endpoints.
    """
    # Step 1: Parse intent
    try:
        response = requests.post(f"{BASE_URL}/intent/", json={"message": user_message})
        if response.status_code != 200:
            print("Failed to parse intent.")
            return

        result = response.json()
        intent = result["intent"]
        data = result["data"]
        next_step = result["next_step"]

        print(f"Intent: {intent}")
        print(f"Next Step: {next_step}")

        # Step 2: Perform next step based on the response
        if next_step == "/search/":
            search_response = requests.post(f"{BASE_URL}{next_step}", json=data)
            print(f"Search Results: {search_response.json()}")
        elif next_step == "/qa/":
            qa_response = requests.post(f"{BASE_URL}{next_step}", json=data)
            print(f"Answer: {qa_response.json()}")
        elif next_step == "/booking/":
            booking_response = requests.post(f"{BASE_URL}{next_step}", json=data)
            print(f"Booking Confirmation: {booking_response.json()}")
        else:
            print("Unhandled next step.")
    except Exception as e:
        print(f"Error handling user message: {e}")
        
def main():
    state = start()
    while state is not None:
        if state == ASSIGN_ENS:
            state = assign_ens()
        elif state == TRAVEL_PLANS:
            state = handle_travel_plans()

if __name__ == '__main__':
    main()