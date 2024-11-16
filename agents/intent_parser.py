from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

load_dotenv()

# Intent Parser Agent
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
intent_parser_prompt = PromptTemplate(
    input_variables=["message"],
    template=(
        "Based on the user message, decide the intent and required action. "
        "Possible intents are: 'search', 'qa', 'book'.\n\n"
        "Message: {message}\n"
        "Return a JSON with fields: 'intent', 'data', and 'next_step'."
    ),
)
intent_parser_chain = LLMChain(llm=llm, prompt=intent_parser_prompt)

def parse_intent(message):
    """
    Parse the user's intent and determine the next step.
    """
    print('in parse_intent')
    try:
        response = intent_parser_chain.run({"message": message})
        intent = response.get('intent')
        data = response.get('data')

        # Define the next step based on the intent
        next_step = None
        if intent == "search":
            next_step = "/search/"
        elif intent == "qa":
            next_step = "/qa/"
        elif intent == "book":
            next_step = "/booking/"
        else:
            next_step = "/intent/"  
        return intent, data, next_step
    except Exception as e:
        return None, None, None
