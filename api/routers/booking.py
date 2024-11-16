from fastapi import APIRouter
from agents.booking_agent import book_hotel

router = APIRouter()

@router.post("/")
async def book_hotel_endpoint(hotel_id: str):
    result = book_hotel(hotel_id)
    return result
