import os
from dotenv import load_dotenv
import argparse
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function 
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Include the system prompt as a model message in the conversation so smaller
# model variants that rely on message history (e.g. flash-lite) correctly
# follow the instruction to make function-call plans.
messages = [
    types.Content(role="model", parts=[types.Part(text=system_prompt)]),
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
]


load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
from google import genai
client = genai.Client(api_key=api_key)

import sys

# Agent loop: call the model repeatedly until it returns a final (non-function) response.
MAX_ITERATIONS = 20
user_prompt = args.user_prompt.replace("\n", "\\n")

for iteration in range(MAX_ITERATIONS):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    prompt_token_count = response.usage_metadata.prompt_token_count
    response_token_count = response.usage_metadata.total_token_count - prompt_token_count
    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {response_token_count}")
        print(f"Iteration {iteration + 1} response:")

    # Add all model candidates to the conversation history so the model can see them
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    # If the model did not request any function calls, it may be either a final
    # human-facing answer or a clarifying question. If the model is asking the
    # user *which file* contains code, proactively inspect the repo so we don't
    # prompt the user for information that already exists in the workspace.
    if not response.function_calls:
        text_lower = (response.text or "").lower()
        clarifying_phrases = ["which file", "what file", "where is", "which file contains"]
        if any(phrase in text_lower for phrase in clarifying_phrases):
            # Fallback: call get_files_info('.') so the agent can see repository files
            class _FC:
                def __init__(self, name, args):
                    self.name = name
                    self.args = args

            fallback_call = _FC("get_files_info", {"directory": "."})
            fallback_result = call_function(fallback_call, verbose=args.verbose)

            # Append the tool result to messages so the model can act on it next
            if fallback_result.parts:
                messages.append(types.Content(role="user", parts=fallback_result.parts))
                # continue to next iteration so the model can use the new info
                continue

        # Not a clarifying question we can auto-resolve — treat as final answer
        print(response.text)
        break

    # Otherwise, call each function the model requested and collect their results
    function_results = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=args.verbose)

        # Validate returned content
        if not function_call_result.parts:
            raise Exception("Function call returned no parts")
        part = function_call_result.parts[0]
        if part.function_response is None or part.function_response.response is None:
            raise Exception("Function call part has no function_response or response")

        function_results.append(part)

        if args.verbose:
            print(f"-> {part.function_response.response}")

    # Append the function results to the conversation so the model can act on them
    messages.append(types.Content(role="user", parts=function_results))

    # Add an explicit follow-up user message to prevent the model from asking the
    # human to perform the listing. This nudges the model to open likely files
    # (README.md, main.py) with `get_file_content` instead of asking for paths.
    messages.append(
        types.Content(
            role="user",
            parts=[
                types.Part(
                    text=(
                        "Tool returned repository listing. Do NOT ask the user for file"
                        " paths — inspect the files and open the most relevant ones"
                        " (e.g. README.md, main.py) with `get_file_content`."
                    )
                )
            ],
        )
    )
else:
    # Max iterations reached without a final answer
    print(f"Error: model did not produce a final response after {MAX_ITERATIONS} iterations.", file=sys.stderr)
    sys.exit(1)