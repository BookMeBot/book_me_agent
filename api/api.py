from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from agents.agent import run_agent

app = FastAPI()

class BookingData(BaseModel):
    location: str = ""
    startDate: int = 0
    endDate: int = 0
    numberOfGuests: int = 0
    numberOfRooms: int = 0
    features: List[str] = []
    budgetPerPerson: int = 0
    currency: str = "USD"

    @property
    def number_of_nights(self) -> int:
        """Calculate the number of nights based on startDate and endDate."""
        if self.startDate and self.endDate:
            return (self.endDate - self.startDate) // 86400  # 86400 seconds in a day
        return 0

    @property
    def total_budget_per_night(self) -> int:
        """Calculate the total budget per night."""
        return self.numberOfGuests * self.budgetPerPerson

    @property
    def total_budget(self) -> int:
        """Calculate the total budget for the stay."""
        return self.total_budget_per_night * self.number_of_nights

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
    if chat_history.booking_data:
        booking_data = chat_history.booking_data.dict()
        # Add calculated properties to the booking data
        booking_data.update({
            "number_of_nights": chat_history.booking_data.number_of_nights,
            "total_budget_per_night": chat_history.booking_data.total_budget_per_night,
            "total_budget": chat_history.booking_data.total_budget
        })
    else:
        booking_data = {}

    # Run the agent logic
    response = run_agent(formatted_messages, booking_data)

    # Return the agent's response along with booking data
    return {
        "responses": response,
        "booking_data": booking_data
    }