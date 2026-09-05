"""
chatbot.py
----------
This is the core chatbot logic — the same logic your CLI version used.
It handles:
1. Loading the Gemini API key securely from .env
2. Sending user questions to Gemini and returning the response
3. Saving user feedback to a text file (simple file handling, as before)

The Flask app (app.py) imports these functions instead of using
input()/print(). The underlying behavior is unchanged.
"""

import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please add it to your .env file."
    )

client = genai.Client(api_key=API_KEY)

# Current model name, per Google's live API error message (Sept 2026)
MODEL_NAME = "gemini-3.6-flash"

FEEDBACK_FILE = "feedback.txt"


def get_response(user_message: str) -> str:
    """
    Sends the user's message to the Gemini API and returns the reply.
    This replaces the old input() -> Gemini -> print() flow.

    Uses the Interactions API (client.interactions.create), which is
    Google's current recommended method and the one documented to work
    with the newer "auth key" (AQ.-prefixed) API keys.
    """
    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=user_message,
        )
        return interaction.output_text.strip()
    except Exception as e:
        return f"Sorry, something went wrong while contacting Gemini: {e}"


def save_feedback(feedback_text: str) -> bool:
    """
    Appends feedback to a local text file.
    Same file-handling approach as the original CLI project —
    just using 'a' (append) mode so old feedback is never overwritten.
    """
    feedback_text = feedback_text.strip()
    if not feedback_text:
        return False

    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        f.write(feedback_text + "\n")

    return True
