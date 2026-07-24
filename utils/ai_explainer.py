import os
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env file
load_dotenv()

# Retrieve API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)