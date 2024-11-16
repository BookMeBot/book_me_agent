import requests
import json

# Define the chat history
chat_history = {
    "name": "Traveler",
    "type": "personal_chat",
    "id": 1234567890,
    "messages": [
        {
            "id": 1,
            "type": "message",
            "date": "2023-08-23T10:00:00",
            "date_unixtime": "1692806400",
            "from": "Traveler",
            "from_id": "user123456",
            "text": "I want to book a hotel in New York for next weekend.",
            "text_entities": [
                {
                    "type": "plain",
                    "text": "I want to book a hotel in New York for next weekend.",
                }
            ],
        },
        {
            "id": 2,
            "type": "message",
            "date": "2023-08-23T10:05:00",
            "date_unixtime": "1692806700",
            "from": "Agent",
            "from_id": "agent123456",
            "text": "Sure, I can help with that. How many nights will you be staying?",
            "text_entities": [
                {
                    "type": "plain",
                    "text": "Sure, I can help with that. How many nights will you be staying?",
                }
            ],
        },
    ],
}

# Send the chat history to the FastAPI endpoint
response = requests.post(
    "http://localhost:8000/chat",
    headers={"Content-Type": "application/json"},
    data=json.dumps(chat_history),
)

# Print the response from the API
print(response.json())
