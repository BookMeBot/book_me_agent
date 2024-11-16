from fastapi import FastAPI, HTTPException
from api.routers import intent, question, search, booking

from pydantic import BaseModel
from agents.intent_parser import parse_intent
from agents.booking_agent import book_hotel

app = FastAPI()

# Register routers
app.include_router(intent.router, prefix="/intent", tags=["Intent"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(question.router, prefix="/qa", tags=["QA"])
app.include_router(booking.router, prefix="/booking", tags=["Booking"])
