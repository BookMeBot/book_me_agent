# Import specific functions or classes to make them available at the package level
from .handlers import start, handle_message
import logging

logging.basicConfig(level=logging.INFO)

# Optionally, define __all__ to control what is imported with 'from package import *'
__all__ = ["start", "handle_message"]
