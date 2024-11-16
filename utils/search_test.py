from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

import getpass
import os

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True,
)

results = tool.invoke(
    {
        "query": "I am looking for a hotel in Chiang Mai thailand for 4 people for 2 rooms on November 20-24 with a budget of $20 per person. I want a pool. Make sure I can book the hotel online. Find me 5 options."
    }
)
print(results)
