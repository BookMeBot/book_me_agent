import json
import os
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure a file to persist the agent's CDP MPC Wallet Data.
wallet_data_file = "wallet_data.txt"

def initialize_agent():
    """Initialize the agent with CDP Agentkit."""
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    wallet_data = None
    if os.path.exists(wallet_data_file):
        with open(wallet_data_file) as f:
            wallet_data = f.read()

    values = {"cdp_wallet_data": wallet_data} if wallet_data else {}
    agentkit = CdpAgentkitWrapper(**values)

    wallet_data = agentkit.export_wallet()
    with open(wallet_data_file, "w") as f:
        f.write(wallet_data)

    cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(agentkit)
    tools = cdp_toolkit.get_tools()

    return create_react_agent(
        llm,
        tools=tools,
        state_modifier="You are the biggest HYPE agent for creating NFTs and memecoins tied to a hotel.",
    )

def create_nft_metadata(booking_data):
    metadata = {
        "name": booking_data.get("name", "Booking NFT"),
        "description": booking_data.get("description", "NFT representing a booking"),
        "attributes": [
            {"trait_type": "Location", "value": booking_data.get("location", "")},
            {"trait_type": "Price Per Night", "value": booking_data.get("price_per_night", "")},
            {"trait_type": "Rating", "value": booking_data.get("rating", "")},
        ],
    }
    return metadata

def create_and_send_nft(agent_executor, booking_data, wallet_addresses):
    metadata = create_nft_metadata(booking_data)
    message_content = {
        "action": "create_and_send_nft",
        "metadata": metadata,
        "wallet_addresses": wallet_addresses
    }
    
    for chunk in agent_executor.stream({"messages": [HumanMessage(content=json.dumps(message_content))]}):
        if "agent" in chunk:
            print(chunk["agent"]["messages"][0].content)
        elif "tools" in chunk:
            print(chunk["tools"]["messages"][0].content)
        print("-------------------")

def main():
    booking_data = {
        "name": "Chiangmai Inn Guest House",
        "location": "Chang Moi, Chiang Mai",
        "price_per_night": "$20",
        "rating": "8.6",
        "description": "Located in Chang Moi, this guest house offers comfortable accommodations with free WiFi access. Guests appreciate its proximity to local attractions and markets.",
    }

    #TODO:change wallet address:
    wallet_addresses = ["wallet_address_1", "wallet_address_2"]
    agent_executor = initialize_agent()
    create_and_send_nft(agent_executor, booking_data, wallet_addresses)

if __name__ == "__main__":
    print("Starting Agent...")
    main()