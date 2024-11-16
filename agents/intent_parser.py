from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import json
import os

load_dotenv()

# Initialize the language model
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

# Define the prompt template with clear instructions and examples
intent_parser_prompt = PromptTemplate(
    input_variables=["message"],
    template=(
        "You are an assistant that determines user intent. Based on the user message, "
        "decide which action to take: 'search', 'question', or 'book'. If the intent is unclear, "
        "default to 'general'.\n\n"
        "User message: {message}\n\n"
        "Respond with a JSON object containing the fields:\n"
        "'intent': one of 'search', 'question', 'book', or 'general',\n"
        "'data': any relevant extracted data (e.g., location, budget, etc.),\n"
        "'next_step': the next logical endpoint for the process (e.g., '/search/').\n\n"
        "Example 1:\n"
        "User message: 'I want to book a hotel in Thailand.'\n"
        "Response:\n"
        "{\n"
        "  \"intent\": \"search\",\n"
        "  \"data\": {\"location\": \"Thailand\"},\n"
        "  \"next_step\": \"/search/\"\n"
        "}\n\n"
        "Example 2:\n"
        "User message: 'Does the hotel have free Wi-Fi?'\n"
        "Response:\n"
        "{\n"
        "  \"intent\": \"question\",\n"
        "  \"data\": {\"amenity\": \"free Wi-Fi\"},\n"
        "  \"next_step\": \"/question/\"\n"
        "}\n\n"
        "Example 3:\n"
        "User message: 'Can you book it for me?'\n"
        "Response:\n"
        "{\n"
        "  \"intent\": \"book\",\n"
        "  \"data\": {\"confirmation\": true},\n"
        "  \"next_step\": \"/booking/\"\n"
        "}\n\n"
        "Example 4:\n"
        "User message: 'Tell me something random.'\n"
        "Response:\n"
        "{\n"
        "  \"intent\": \"general\",\n"
        "  \"data\": {},\n"
        "  \"next_step\": \"/general/\"\n"
        "}"
    ),
)

def parse_intent(message):
    """
    Determines the user's intent and routes to the appropriate agent.
    """
    try:
        # Generate the model's response
        response = llm.generate(prompt=intent_parser_prompt.format(message=message))
        print(f"Raw response: {response}")  # Debugging: Inspect raw response

        # Parse the response as JSON
        response_data = json.loads(response)

        # Extract fields from the response
        intent = response_data.get("intent")
        data = response_data.get("data", {})
        next_step = response_data.get("next_step")

        # Validate the extracted fields
        if intent not in {"search", "question", "book", "general"} or not next_step:
            raise ValueError("Invalid response structure or intent.")

        return intent, data, next_step
    except json.JSONDecodeError:
        print(f"Error: Response not valid JSON:\n{response}")
        return "general", {}, "/general/"
    except Exception as e:
        print(f"Error parsing intent: {e}")
        return "general", {}, "/general/"

if __name__ == "__main__":
    test_messages = [
        "I want to book a hotel in Thailand.",
        "Does the hotel have free Wi-Fi?",
        "Can you book it for me?",
        "Tell me something random.",
    ]

    for message in test_messages:
        intent, data, next_step = parse_intent(message)
        print(f"Message: {message}")
        print(f"Intent: {intent}")
        print(f"Data: {data}")
        print(f"Next Step: {next_step}")
        print("-" * 50)
