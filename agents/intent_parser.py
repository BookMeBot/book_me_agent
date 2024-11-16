from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import json
import os

# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

# Define the prompt template
intent_parser_prompt = PromptTemplate(
    input_variables=["message"],
    template=(
        "You are an intent parser agent that decides which subagent should handle a user request. "
        "Possible agents are:"
        "'intent': For deciding where to route the agents - the home controller agent that is in charge of routing."
        "'search': For searches based on user preferences."
        "'question': For answering specific questions about travel (e.g., Wi-Fi, area, tips)."
        "'booking': For booking a travel plan based on confirmed user feedback."
        ""
        "User message: {message}"
        "Respond strictly with a JSON object in this format:"
        "{"
        "  'intent': 'intent' | 'search' | 'question' | 'booking',"
        "  'data': {...},"
        "  'next_step': '/intent/' | '/search/' | '/question/' | '/booking/'"
        "}"
        "Ensure the output is a valid JSON object without any additional text."
    ),
)

function_schema = {
    "name": "parse_intent",
    "description": "Parse user message to determine intent and route. You are an intent parser agent that decides which subagent should handle a user request. "
    "Possible agents are:"
    "intent: For deciding where to route the agents - the home controller agent that is in charge of routing."
    "search: For searches based on user preferences."
    "question: For answering specific questions about travel (e.g., Wi-Fi, area, tips)."
    "booking: For booking a travel plan based on confirmed user feedback.",
    "parameters": {
        "type": "object",
        "properties": {
            "intent": { 
                "type": "string",
                "enum": ["intent", "search", "question", "booking"],
                "description": "The determined intent of the user message.",
            },
            "data": {
                "type": "object",
                "description": "Relevant extracted data, e.g., location, amenities.",
            },
            "next_step": {
                "type": "string",
                "enum": ["/intent/", "/search/", "/question/", "/booking/"],
                "description": "The endpoint to route based on intent.",
            },
        },
        "required": ["message"],
    },
}

# Initialize the language model with function calling capability
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"),
    functions=[function_schema],
    function_call={"name": "parse_intent"},
)


def parse_intent(message):
    """
    Determines the user's intent and routes to the appropriate subagent.
    """
    print(f"Debug: Received message for parsing: {message}")

    try:
        # Prepare the input for the model
        input_message = {"role": "user", "content": message}

        # Generate the model's response
        response = llm.invoke([input_message])
        print(f"Debug: Raw response from LLM:\n{response}")  # Log the raw response

        # Access the function call from the response
        function_call = response.additional_kwargs.get("function_call")
        if not function_call:
            raise ValueError("No function call returned by the model.")

        # Parse the arguments of the function call
        function_args = function_call.get("arguments")
        if not function_args:
            raise ValueError("No function call arguments returned by the model.")

        # Convert arguments from string to JSON
        response_data = json.loads(function_args)

        # Extract fields from the response
        intent = response_data.get("intent")
        data = response_data.get(
            "data", {}
        )  # Default to an empty dict if data is missing
        next_step = response_data.get("next_step")

        # Validate extracted fields
        if not intent or intent not in {"intent", "search", "question", "booking"}:
            print(f"Error: Missing or invalid 'intent' in response:\n{response_data}")
            raise ValueError("Invalid intent in response.")
        if not next_step:
            print(f"Error: Missing 'next_step' in response:\n{response_data}")
            raise ValueError("Invalid next_step in response.")

        return intent, data, next_step

    except Exception as e:
        print(f"Error parsing intent: {e}")
        raise ValueError("An error occurred during intent parsing.")
