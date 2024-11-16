import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Client(api_key=ANTHROPIC_API_KEY)


def check_and_return_payload(data):
    required_fields = [
        "location",
        "startDate",
        "endDate",
        "numberOfGuests",
        "numberOfRooms",
        "budgetPerPerson",
        "currency",
    ]

    # Check if all required fields are present and not None
    missing_fields = [field for field in required_fields if not data.get(field)]

    if not missing_fields:
        # All fields are present
        return {
            "data": {
                "chatId": "-4555870136",
                "completedData": True,
                "response": {"requestData": data},
            }
        }
    else:
        # Some fields are missing
        return {
            "data": {
                "chatId": "-4555870136",
                "completedData": False,
                "response": f"We need more data: {', '.join(missing_fields)}",
            }
        }


def run_agent(messages, booking_data):
    # Initial user message
    messages.append(
        {
            "role": "user",
            "content": """Welcome to BookMeBot! Let's plan your next trip 🏖 To help us find the best options for you, please provide the following details:

    1. **Location**: Where would you like to stay? (e.g., New York City, Paris)
    2. **Dates**: What are your check-in and check-out dates? (e.g., Check-in: 2025-09-15, Check-out: 2025-09-20)
    3. **Price Range**: What is your budget per person? (e.g., $100 per night)
    4. **Amenities**: Are there any specific amenities you desire? (e.g., Pool, Free Wi-Fi, Gym)
    5. **Number of Guests**: How many people will be staying? (e.g., 2 adults)

    Feel free to provide any additional preferences or requirements you might have. Let's make your stay unforgettable! 🏖️
    """,
        }
    )

    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=[
                {
                    "name": "search",
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

        tool_name = "unknown"
        # Check if a valid function was called
        if response.stop_reason == "tool_use":
            if response.content and isinstance(response.content[0], dict):
                tool_name = response.content[0].get("name", "unknown")
            if tool_name == "search":
                print("Function called: search")
                payload = check_and_return_payload(booking_data)
                print(payload)
                tool_result = {
                    "role": "tool_result",
                    "content": "Hotel search results: Hotel A, Hotel B, Hotel C",
                }
                messages.append(tool_result)
            elif tool_name == "booking":
                print("Function called: booking")
                # Simulate a tool result
                tool_result = {
                    "role": "tool_result",
                    "content": "Hotel booking confirmed for Hotel A. Transaction ID: 123456",
                }
                messages.append(tool_result)
            elif tool_name == "question":
                print("Function called: question")
                # Simulate a tool result
                tool_result = {
                    "role": "tool_result",
                    "content": "Please provide more details about your preferences.",
                }
                messages.append(tool_result)
            elif tool_name == "answer":
                print("Function called: answer")
                # Simulate a tool result
                tool_result = {
                    "role": "tool_result",
                    "content": "The area is known for its beautiful beaches.",
                }
                messages.append(tool_result)
            continue  # Continue the loop to process the next message

        # If no function was called, prompt the LLM to call a function
        messages.append(
            {
                "role": "user",
                "content": "Please call one of these functions: search, booking, question, answer.",
            }
        )

        # If a function was called with invalid input, notify the LLM
        if response.is_error:
            messages.append(
                {
                    "role": "user",
                    "content": f"You called function '{tool_name}' with invalid input. Please provide the correct input.",
                }
            )

        # Break the loop if no further action is needed
        if not response.stop_reason == "tool_use":
            break

    return messages


def main():
    messages = []
    print("Welcome to the CLI chat with BookMeBot!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break
        messages.append({"role": "user", "content": user_input})
        # Example booking data
        booking_data = {
            "location": "New York City",
            "startDate": 1692806400,
            "endDate": 1692892800,
            "numberOfGuests": 2,
            "numberOfRooms": 1,
            "features": ["Wi-Fi", "swimming pool"],
            "budgetPerPerson": 150,
            "currency": "USD",
        }
        responses = run_agent(messages, booking_data)
        for response in responses:
            if response["role"] == "assistant":
                print(f"Bot: {response['content']}")


if __name__ == "__main__":
    main()
