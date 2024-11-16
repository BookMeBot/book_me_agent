import os
from dotenv import load_dotenv

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
load_dotenv()
# Intent Parser Agent
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
intent_parser_prompt = PromptTemplate(
    input_variables=["message"],
    template=(
        "Extract structured travel information from the following message:\n"
        "{message}\n\n"
        "Return a JSON with the following fields: 'location', 'budget', 'dates', "
        "'duration', 'number_of_rooms', 'neighborhood', and 'features' (e.g., Wi-Fi, pool). "
        "If information is missing, return None for the missing fields."
    ),
)
intent_parser_chain = intent_parser_prompt | llm

def parse_intent(message):
    try:
        # Use the LLMChain's method to execute the chain
        response = intent_parser_chain({"message": message})
        print(f"Response: {response}")  # Debug statement
        # Assuming the response is a dictionary with 'intent' and 'data' keys
        intent = response.get('intent', None)
        data = response.get('data', None)
        return intent, data
    except Exception as e:
        print(f"Error in parse_intent: {e}")  # Log the error
        return None, None