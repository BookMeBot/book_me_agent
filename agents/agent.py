import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

def run_agent(messages):
    # Initial user message
    messages.append(
        {
            "role": "user",
            "content": "Welcome to BookMeBot! Let's plan your next trip 🏖 Where do you want to go?",
        }
    )

    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=[
                {
                    "name": "search_agent",
                    "description": "Search for hotels based on booking data and user feedback.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "booking_data": {
                                "type": "string",
                                "description": "Booking data, never null.",
                            },
                            "user_feedback": {
                                "type": "string",
                                "description": "User feedback data, can be null.",
                            },
                        },
                        "required": ["booking_data"],
                    },
                },
                {
                    "name": "booking",
                    "description": "Book a hotel based on user preferences.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "hotel_id": {
                                "type": "string",
                                "description": "ID of the hotel to book.",
                            }
                        },
                        "required": ["hotel_id"],
                    },
                },
                {
                    "name": "question",
                    "description": "Ask the user for more information if key info is missing.",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "Question to ask the user.",
                            }
                        },
                        "required": ["question"],
                    },
                },
                {
                    "name": "answer",
                    "description": "Answer random questions like 'What is the area like?'",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The question to answer.",
                            }
                        },
                        "required": ["query"],
                    },
                },
            ],
            messages=messages,
        )

        # Append the assistant's response to the message history
        messages.append({"role": "assistant", "content": response.content})

        tool_name = "unknown"
        # Check if a valid function was called
        if response.stop_reason == "tool_use":
            if response.content and isinstance(response.content[0], dict):
                tool_name = response.content[0].get("name", "unknown")
            if tool_name == "search_agent":
                # Handle search agent logic
                pass
            elif tool_name == "booking":
                # Handle booking logic
                pass
            elif tool_name == "question":
                # Handle question logic
                pass
            elif tool_name == "answer":
                # Handle answer logic
                pass
            break

        # If no function was called, prompt the user to call a function
        messages.append(
            {
                "role": "user",
                "content": "Please call one of these functions: search_agent, booking, question, answer.",
            }
        )

        # If a function was called with invalid input, notify the user
        if response.is_error:
            messages.append(
                {
                    "role": "user",
                    "content": f"You called function '{tool_name}' with invalid input. Please provide the correct input.",
                }
            )

    return messages