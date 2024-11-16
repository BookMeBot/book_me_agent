import os
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
        print("Sorry, that's an invalid response.