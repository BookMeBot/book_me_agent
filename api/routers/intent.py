from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from agents.intent_parser import parse_intent

router = APIRouter()


class IntentRequest(BaseModel):
    message: str


@router.post("/")
async def parse_intent_endpoint(request: IntentRequest):
    intent, data, next_step = parse_intent(request.message)
    if not intent:
        raise HTTPException(status_code=400, detail="Could not determine intent.")
    return {"intent": intent, "data": data, "next_step": next_step}
