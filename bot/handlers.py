import os
from telegram import __version__ as tg_version
from telegram.ext import CallbackContext, ConversationHandler, Updater, CommandHandler, MessageHandler, filters 
from agents.intent_parser import parse_intent
from agents.search_agent import search_hotels
from agents.qa_agent import answer_question
from cdp_agentkit_core.actions.register_basename import register_basename

#Define states
CREATE_WALLET, ASSIGN_ENS, TRAVEL_PLANS = range(3)

user_data = {}

def start(update: Updater, context: CallbackContext) -> int:
    chat_id = update.message.chat_id

    # Create a new wallet for the user using CdpAgentkitWrapper
    agentkit = CdpAgentkitWrapper()
    user_wallet = agentkit.export_wallet()
    user_data[chat_id] = {'wallet': user_wallet}

    update.message.reply_text(
        f"Welcome! A new wallet has been created for you. Your wallet address is {user_wallet['default_address_id']}.\n"
        "Please provide a unique ENS domain name for your agent:"
    )
    return ASSIGN_ENS

def assign_ens(update: Updater, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    ens_name = update.message.text.strip()
    user_wallet = user_data[chat_id]['wallet']

    try:
        # Register the ENS domain
        register_basename(user_wallet, ens_name)
        user_data[chat_id]['ens_domain'] = ens_name
        update.message.reply_text(
            f"ENS domain '{ens_name}' has been assigned to your wallet.\n"
            "You can now proceed with your travel plans. Where would you like to go?"
        )
        return TRAVEL_PLANS
    except Exception as e:
        update.message.reply_text(
            f"An error occurred while registering the ENS domain: {e}\n"
            "Please provide a different ENS domain name:"
        )
        return ASSIGN_ENS

def handle_travel_plans(update: Updater, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    user_message = update.message.text

    parsed_intent = parse_intent(user_message)
    if not parsed_intent:
        update.message.reply_text("Sorry, that's an invalid response. Please provide more details.")
        return TRAVEL_PLANS

    hotel_options = search_hotels(parsed_intent)
    if hotel_options:
        options_text = "\n".join([f"{i+1}. {option}" for i, option in enumerate(hotel_options)])
        update.message.reply_text(f"Here are some options:\n{options_text}")
    else:
        update.message.reply_text("No hotel options found matching your criteria.")

    return ConversationHandler.END

def handle_message(update: Updater, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_message = update.message.text

    # Parse the user's intent
    intent, data = parse_intent(user_message)

    if intent:
        # Respond based on the parsed intent
        update.message.reply_text(f"Intent: {intent}\nData: {data}")
    else:
        # If no intent is found, ask for more information
        update.message.reply_text("I'm not sure what you mean. Could you provide more details?")

def main():
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASSIGN_ENS: [MessageHandler(filters.TEXT & ~filters.COMMAND, assign_ens)],
            TRAVEL_PLANS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_travel_plans)],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()