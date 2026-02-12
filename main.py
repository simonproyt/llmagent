import os
from dotenv import load_dotenv
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions 
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
    contents=messages,
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
))
prompt_token_count = response.usage_metadata.prompt_token_count
response_token_count = response.usage_metadata.total_token_count - prompt_token_count
user_prompt = args.user_prompt.replace("\n", "\\n")
if args.verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {response_token_count}")
    print("Response:")

# If the model returned function calls, print each name and args; otherwise print the text
if response.function_calls:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
else:
    print(response.text)