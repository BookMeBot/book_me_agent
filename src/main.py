import os
from anthropic import Anthropic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class BookingRequest(BaseModel):
    location: str
    check_in: str
    check_out: str
    guests: int
    wallet_private_key: Optional[str] = None


def setup_metamask_message(private_key: str):
    return {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"""Please help me set up MetaMask with a private key and connect to Travala. Follow these steps:
                1. Open MetaMask extension
                2. Click on the account menu (circle icon in top-right)
                3. Select 'Import Account'
                4. Enter the private key: {private_key}
                5. Complete the import""",
            },
            {
                "type": "computer_use",
                "computerUse": {
                    "type": "browser",
                    "capabilities": ["navigate", "click", "type", "extract"],
                },
            },
        ],
    }


def initialize_travala_booking_message():
    return {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": """Now let's proceed with Travala booking:
                1. Navigate to Travala.com
                2. Click 'Login/Register'
                3. Select 'Continue with Web3 Wallet'
                4. Choose MetaMask
                5. Accept the connection request""",
            },
            {
                "type": "computer_use",
                "computerUse": {
                    "type": "browser",
                    "capabilities": ["navigate", "click", "type", "extract"],
                },
            },
        ],
    }


@app.post("/book_hotel")
async def book_hotel(booking_request: BookingRequest):
    try:
        messages = []

        # If private key is provided, set up MetaMask first
        if booking_request.wallet_private_key:
            messages.append(setup_metamask_message(booking_request.wallet_private_key))

        # Initialize Travala booking process
        messages.append(initialize_travala_booking_message())

        # Add booking details
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Search for a hotel with these criteria:
                    Location: {booking_request.location}
                    Check-in: {booking_request.check_in}
                    Check-out: {booking_request.check_out}
                    Number of guests: {booking_request.guests}""",
                    }
                ],
            }
        )

        # Create a message to Claude
        response = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=messages,
            temperature=0,
        )

        return {"status": "success", "response": response.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
