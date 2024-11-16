# Environment variable management setup
import os
from dotenv import load_dotenv
import getpass

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRåAM_BOT_TOKEN")
CDP_API_KEY_NAME = os.getenv("CDP_API_KEY_NAME")
CDP_API_KEY_PRIVATE_KEY = os.getenv("CDP_API_KEY_PRIVATE_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
