import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.declerations import available_functions
from functions.handler import handle_function_call
from prompt import system_prompt


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--verbose")]

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Please set the GEMINI_API_KEY environment variable in .env")
        sys.exit(1)

    if not args:
        print("Usage: python main.py <prompt> [--verbose]")
        print('Example: python main.py "What is the capital of France?"')
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    prompt = str.join(" ", args)

    if verbose:
        print(f"User prompt: {prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    generate_response(client, messages, verbose)


def generate_response(client, messages, verbose):
    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )

    if verbose:
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")

    if res.function_calls:
        for function_call_part in res.function_calls:
            func_res = handle_function_call(function_call_part, verbose)

            if not func_res.parts[0].function_response.response:
                raise Exception(f"Error calling function: {function_call_part.name}")

            if verbose:
                print(f"-> {func_res.parts[0].function_response.response}")

    if res.text:
        print("Response:")
        print(res.text)


if __name__ == "__main__":
    main()
