from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.intent_parser import parse_intent

router = APIRouter()


class IntentRequest(BaseModel):
    message: str


@router.post("/")
async def parse_intent_endpoint(request: IntentRequest):
    print("Debug: Received request to parse intent")  # Debug statement
    try:
        intent, data, next_step = parse_intent(request.message)
        return {"intent": intent, "data": data, "next_step": next_step}
    except ValueError as e:
        print(f"Debug: ValueError occurred: {e}")  # Debug statement
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Debug: Exception occurred: {e}")  # Debug statement
        raise HTTPException(status_code=500, detail="Internal server error.")
