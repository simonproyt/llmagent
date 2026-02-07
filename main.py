import os
from dotenv import load_dotenv
import argparse
from google.genai import types
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
from google import genai
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages
    )
prompt_token_count = response.usage_metadata.prompt_token_count
response_token_count = response.usage_metadata.total_token_count - prompt_token_count
user_prompt = args.user_prompt.replace("\n", "\\n")
print(f"User prompt: {user_prompt}")
print(f"Prompt tokens: {prompt_token_count}")
print(f"Response tokens: {response_token_count}")
print("Response:")
print(response.text)