import anthropic
import os

def internet_search(query):
    # Initialize the Claude client
    client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Define the prompt for Claude
    prompt = f"""
    You are a virtual assistant with the ability to browse the internet. Please perform a web search for the following query and provide a concise summary of the top results:

    Query: "{query}"

    Provide the summary in a clear and concise manner.
    """

    # Send the prompt to Claude
    response = client.completion(
        prompt=prompt,
        model="claude-3.5-sonnet",
        max_tokens=300,
        temperature=0.7,
        stop_sequences=["\n\n"]
    )

    # Extract and return the summary from Claude's response
    summary = response['completion'].strip()
    return summary

# TODO: Add claude web browsing 
def book_hotel(hotel_id):
    #TODO: Use claude 3.5 computer use to browse with remote server
    print("Stub: Booking completed!")