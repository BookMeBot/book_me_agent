from langchain.tools import BaseTool

class HotelSearchTool(BaseTool):
    name: str = "SearchHotels"
    description: str = "Searches for hotels given a dictionary of search criteria."

    def _run(self, search_criteria: dict) -> str:
        # Extract parameters from the dictionary
        location = search_criteria.get("location")
        budget = search_criteria.get("budget")
        preferences = search_criteria.get("preferences")
        
        # Implement hotel search logic using the extracted parameters
        return "List of hotels based on the search criteria"