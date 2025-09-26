import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini client with the API key
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("Error: GEMINI_API_KEY not found. Make sure it's set in your .env file.")
    
    genai.configure(api_key=gemini_api_key)
    
    # Initialize the Generative Model
    # Using gemini-1.5-flash which is fast and powerful
    model = genai.GenerativeModel('gemini-1.0-pro')

except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    model = None

def ask_ai(prompt: str) -> str:
    """
    Sends a prompt to the Google Gemini API and returns the model's response.
    """
    if model is None:
        return "Google Gemini client is not initialized. Check your API key and logs."

    try:
        # Generate content using the model
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Handle potential API errors
        return f"An error occurred with the Gemini AI service: {e}"