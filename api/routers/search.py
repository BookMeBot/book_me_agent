from fastapi import APIRouter
from agents.search_agent import search_hotels

router = APIRouter()

@router.post("/")
async def search_hotels_endpoint(search_criteria: dict):
    results = search_hotels(search_criteria)
    return {"results": results}
