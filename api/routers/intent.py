from fastapi import APIRouter, HTTPException
from agents.intent_parser import parse_intent

router = APIRouter()

@router.post("/")
async def parse_intent_endpoint(message: str):
    """
    Endpoint for parsing user intent.
    """
    intent, data, next_step = parse_intent(message)
    if not intent:
        raise HTTPException(status_code=400, detail="Could not determine intent.")
    return {"intent": intent, "data": data, "next_step": next_step}
