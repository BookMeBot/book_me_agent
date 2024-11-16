# coinbase_agent.py
import json
import os
import sys
import time

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Import CDP Agentkit Langchain Extension.
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
from cdp_langchain.tools import CdpTool
from pydantic import BaseModel, Field
from cdp import *
import os
from dotenv import load_dotenv

hotels = [
    {
        "name": "Chiangmai Inn Guest House",
        "location": "Chang Moi, Chiang Mai",
        "price_per_night": "$20",
        "rating": "8.6",
        "description": "Located in Chang Moi, this guest house offers comfortable accommodations with free WiFi access. Guests appreciate its proximity to local attractions and markets.",
    },
    {
        "name": "33 Poshtel",
        "location": "Hai Ya, Chiang Mai",
        "price_per_night": "$25",
        "rating": "8.5",
        "description": "Situated in the Hai Ya district, 33 Poshtel provides modern rooms with air conditioning and free WiFi. The property features an outdoor pool and a shared lounge.",
    },
    {
        "name": "Thapae Gate Lodge",
        "location": "Phra Sing, Chiang Mai",
        "price_per_night": "$20",
        "rating": "9.0",
        "description": "Well set in the center of Chiang Mai, Thapae Gate Lodge offers air-conditioned rooms, a garden, free WiFi, and a terrace. Guests praise its convenient location and friendly staff.",
    },
    {
        "name": "Pissamorn House",
        "location": "Phra Sing, Chiang Mai",
        "price_per_night": "$25",
        "rating": "9.3",
        "description": "Located in the center of the old city area, Pissamorn House offers free WiFi access and is known for its clean and comfortable rooms.",
    },
    {
        "name": "All in 1 Guesthouse",
        "location": "Phra Sing, Chiang Mai",
        "price_per_night": "$24",
        "rating": "9.0",
        "description": "Situated in a charming street with plenty of quiet bars and eateries, All in 1 Guesthouse offers simple accommodations with friendly service.",
    },
    {
        "name": "Paapu House",
        "location": "Chang Moi, Chiang Mai",
        "price_per_night": "$29",
        "rating": "9.6",
        "description": "Paapu House provides a clean and charming space with a back deck that stays cool from the sun all day, offering a nice quiet spot to relax.",
    },
    {
        "name": "Ban Pongphan",
        "location": "Hai Ya, Chiang Mai",
        "price_per_night": "$20",
        "rating": "9.5",
        "description": "Great location between the airport and old town, Ban Pongphan offers affordable accommodations with a night market opposite and many supermarkets around.",
    },
    {
        "name": "Ma Guesthouse Chiang Mai",
        "location": "Phra Sing, Chiang Mai",
        "price_per_night": "$20",
        "rating": "9.0",
        "description": "Ma Guesthouse offers clean and comfortable rooms with friendly staff, located in a convenient area close to local attractions.",
    },
    {
        "name": "Hidden Garden Hostel",
        "location": "Hai Ya, Chiang Mai",
        "price_per_night": "$36",
        "rating": "9.0",
        "description": "Hidden Garden Hostel provides spacious beds in dorms with plugs and curtains for privacy. Guests appreciate the clean facilities and helpful staff.",
    },
    {
        "name": "MD House",
        "location": "Si Phum, Chiang Mai",
        "price_per_night": "$34",
        "rating": "7.8",
        "description": "MD House offers lovely accommodations in the heart of Chiang Mai, with a receptionist who is a great host and helps with any problems.",
    },
]

# Load environment variables
load_dotenv()

# Configure a file to persist the agent's CDP MPC Wallet Data.
wallet_data_file = "wallet_data.txt"

def initialize_agent():
    """Initialize the agent with CDP Agentkit."""
    # Initialize LLM.
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    wallet_data = None

    if os.path.exists(wallet_data_file):
        with open(wallet_data_file) as f:
            wallet_data = f.read()

    # Configure CDP Agentkit Langchain Extension.
    values = {}
    if wallet_data is not None:
        # If there is a persisted agentic wallet, load it and pass to the CDP Agentkit Wrapper.
        values = {"cdp_wallet_data": wallet_data}

    agentkit = CdpAgentkitWrapper(**values)

    # persist the agent's CDP MPC Wallet Data.
    wallet_data = agentkit.export_wallet()
    with open(wallet_data_file, "w") as f:
        f.write(wallet_data)

    # Initialize CDP Agentkit Toolkit and get tools.
    cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(agentkit)
    tools = cdp_toolkit.get_tools()

    # Store buffered conversation history in memory.
    memory = MemorySaver()
    config = {"configurable": {"thread_id": "CDP Agentkit Chatbot Example!"}}

    # Create ReAct Agent using the LLM and CDP Agentkit tools.
    return (
        create_react_agent(
            llm,
            tools=tools,
            checkpointer=memory,
            state_modifier="You are the biggest HYPE agent for creating NFTs and memecoins tied to a hotel. I want you to create fun and engaging content. You are empowered to interact onchain using your tools. If you ever need funds, you can request them from the faucet if you are on network ID `base-sepolia`. Create NFT collections for hotels in Chiang Mai. Here is the list: {hotels}. If not, you can provide your wallet details and request funds from the user. If someone asks you to do something you can't do with your currently available tools, you must say so, and encourage them to implement it themselves using the CDP SDK + Agentkit, recommend they go to docs.cdp.coinbase.com for more informaton. Be concise and helpful with your responses. Refrain from restating your tools' descriptions unless it is explicitly requested.",
        ),
        config,
    )

# Autonomous Mode
def run_autonomous_mode(agent_executor, config, interval=10):
    """Run the agent autonomously with specified intervals."""
    print("Starting autonomous mode...")
    while True:
        try:
            # Provide instructions autonomously
            thought = (
                "Be creative and do something interesting on the blockchain. "
                "Choose an action or set of actions and execute it that highlights your abilities."
            )

            # Run agent in autonomous mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=thought)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

            # Wait before the next action
            time.sleep(interval)

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)

# Chat Mode
def run_chat_mode(agent_executor, config):
    """Run the agent interactively based on user input."""
    print("Starting chat mode... Type 'exit' to end.")
    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() == "exit":
                break

            # Run agent with the user's input in chat mode
            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

        except KeyboardInterrupt:
            print("Goodbye Agent!")
            sys.exit(0)

# Mode Selection
def choose_mode():
    """Choose whether to run in autonomous or chat mode based on user input."""
    while True:
        print("\nAvailable modes:")
        print("1. chat    - Interactive chat mode")
        print("2. auto    - Autonomous action mode")

        choice = input("\nChoose a mode (enter number or name): ").lower().strip()
        if choice in ["1", "chat"]:
            return "chat"
        elif choice in ["2", "auto"]:
            return "auto"
        print("Invalid choice. Please try again.")

def main():
    """Start the chatbot agent."""
    agent_executor, config = initialize_agent()

    mode = choose_mode()
    if mode == "chat":
        run_chat_mode(agent_executor=agent_executor, config=config)
    elif mode == "auto":
        run_autonomous_mode(agent_executor=agent_executor, config=config)

if __name__ == "__main__":
    print("Starting Agent...")
    main()