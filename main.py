import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions
import json

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("Invalid API Key")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    response = client.chat.completions.create(
        model = "openrouter/free",
        messages = messages,
        tools = available_functions,
    )

    usage = response.usage
    if usage is None:
        raise RuntimeError("Failed API Request")

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_tokens}")
        print(f"Response tokens: {usage.completion_tokens}")
    print(response.choices[0].message.content)

    message = response.choices[0].message
    for tool_call in message.tool_calls:
        function_agrs = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_agrs})")

if __name__ == "__main__":
    main()
