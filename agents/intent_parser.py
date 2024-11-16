from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import json
import os

load_dotenv()

# Initialize the language model
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

# Define the prompt template
intent_parser_prompt = PromptTemplate(
    input_variables=["message"],
    template=(
        "You are an intent parser agent that decides which subagent should handle a user request. "
        "Possible agents are:\n"
        "'search': For searches based on user preferences.\n"
        "'question': For answering specific questions about travel (e.g., Wi-Fi, area, tips).\n"
        "'booking': For booking a travel plan based on confirmed user feedback.\n"
        "\n"
        "User message: {message}\n\n"
        "Respond with a JSON object containing:\n"
        "{\n"
        "  'intent': 'search', 'question', or 'booking',\n"
        "  'data': {relevant extracted data, e.g., location, amenities},\n"
        "  'next_step': '/search/', '/question/', or '/booking/' based on intent.\n"
        "}"
    ),
)


def parse_intent(message):
    """
    Determines the user's intent and routes to the appropriate subagent.
    """
    print(f"Debug: Received message for parsing: {message}")

    try:
        # Generate the model's response
        response = llm.predict(intent_parser_prompt.format(message=message))
        print(f"Raw response: {response}")  # Debugging: Inspect raw response

        # Parse the response as JSON
        response_data = json.loads(response)

        # Extract fields from the response
        intent = response_data.get("intent")
        data = response_data.get("data", {})
        next_step = response_data.get("next_step")

        if intent not in {"search", "question", "booking"} or not next_step:
            raise ValueError("Invalid intent or next_step in response.")

        return intent, data, next_step
    except json.JSONDecodeError:
        print(f"Error: Response not valid JSON:\n{response}")
        raise ValueError("Failed to determine intent.")
    except Exception as e:
        print(f"Error parsing intent: {e}")
        raise ValueError("An error occurred during intent parsing.")


