from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.agent import run_agent  # Import the function to run the agent

app = FastAPI()


class ChatHistory(BaseModel):
    name: str
    type: str
    id: int
    messages: list


@app.post("/chat")
async def chat_endpoint(chat_history: ChatHistory):
    # Extract messages from the chat history
    messages = chat_history.messages

    # Convert messages to the format expected by the agent
    formatted_messages = [
        {"role": "user", "content": message["text"]} for message in messages
    ]

    # Run the agent logic
    response = run_agent(formatted_messages)

    # Return the agent's response
    return {"responses": response}
