from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from agents.agent import run_agent  

app = FastAPI()

class BookingData(BaseModel):
    location: str = ""
    startDate: int = 0
    endDate: int = 0
    numberOfGuests: int = 0
    numberOfRooms: int = 0
    features: list = []
    budgetPerPerson: int = 0
    currency: str = "USD"

class ChatHistory(BaseModel):
    name: str
    type: str
    id: int
    messages: list
    booking_data: Optional[BookingData] = None  # Make booking_data optional

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/chat")
async def chat_endpoint(chat_history: ChatHistory):
    # Extract messages from the chat history
    messages = chat_history.messages

    # Convert messages to the format expected by the agent
    formatted_messages = [
        {"role": "user", "content": message["text"]} for message in messages
    ]

    # Extract booking data if available
    booking_data = chat_history.booking_data.dict() if chat_history.booking_data else {}

    # Run the agent logic
    response = run_agent(formatted_messages, booking_data)

    # Return the agent's response along with booking data
    print("returning from return", {
        "responses": response,
        "booking_data": booking_data})
    return {
        "responses": response,
        "booking_data": booking_data
    }