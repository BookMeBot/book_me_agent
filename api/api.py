from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.intent_parser import parse_intent
from agents.booking_agent import book_hotel

app = FastAPI()

class IntentRequest(BaseModel):
    message: str
    chat_history: str  

class BookingRequest(BaseModel):
    hotel_id: str
    chat_history: str  

@app.post("/parse-intent/")
async def parse_intent_endpoint(request: IntentRequest):
    intent, data = parse_intent(request.message)
    if intent is None:
        raise HTTPException(status_code=400, detail="Could not parse intent")
    return {"intent": intent, "data": data}

@app.post("/book-hotel/")
async def book_hotel_endpoint(request: BookingRequest):
    # Assuming book_hotel is a stub and returns a success message
    book_hotel(request.hotel_id)
    return {"status": "success", "message": "Hotel booked successfully!"}

# Run the application
# Use the command: uvicorn api:app --reload