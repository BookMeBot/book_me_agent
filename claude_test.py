import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Anthropic client

client = anthropic.Client(
    api_key="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"
)
print(client)
# Define variables for flexibility
MODEL_VERSION = "claude-3-5-sonnet-20241022"
MAX_TOKENS = 1024
TASK_DESCRIPTION = (
    "Save a picture of a dog to my documents folder."  # Task description variable
)
BETA_VERSION = "computer-use-2024-10-22"  # Beta feature version

# Send the request with flexible parameters
response = client.beta.messages.create(
    model=MODEL_VERSION,
    max_tokens=MAX_TOKENS,
    tools=[
        {
            "type": "computer_20241022",
            "name": "computer",
            "display_width_px": 1024,
            "display_height_px": 768,
            "display_number": 1,
        },
        {"type": "text_editor_20241022", "name": "str_replace_editor"},
        {"type": "bash_20241022", "name": "bash"},
    ],
    messages=[{"role": "user", "content": TASK_DESCRIPTION}],
    betas=[BETA_VERSION],
)

print(response)
