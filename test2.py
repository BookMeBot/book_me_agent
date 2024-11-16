import anthropic
import os

client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
# print("end", os.getenv("ANTHROPIC_API_KEY"))

messages = [{"role": "user", "content": "fuck you"}]
while true: 
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=[
            {
                "name": "get_weather",
                "description": "Get the current weather in a given location",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        }
                    },
                    "required": ["location"],
                },
            }
        ],
        messages=messages,
    )
    print(response)

    messages.append(response.newAssitantMessage)

    // if a valid function was called, handle it and break from the loop
    // one of functons is ask user for more info 


    // if no function was called, add another user message saying "Please call one of these functions: booking, ..."
    # messages = [{"role": "user", "content": "fuck you"}]

    // if a function was called with invalid input, say "you called function 'booking' with invalid input, make sure to use input ..."

# //latest message in the chat in the prompt what do you think user wants to do between these things
# example telegram convo 