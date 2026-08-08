import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json
import sys

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
    for _ in range(20):
        response = client.chat.completions.create(
            model = "openrouter/free",
            messages = messages,
            tools = available_functions,
            temperature = 0,
        )

        usage = response.usage
        if usage is None:
            raise RuntimeError("Failed API Request")

        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage.prompt_tokens}")
            print(f"Response tokens: {usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print(f"Final response:\n{message.content}")
            break

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call)
            messages.append(result_message)
            if result_message['content'] is None:
                raise Exception("No content")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print("Maximum iterations reached without a final response")
        sys.exit(1)
if __name__ == "__main__":
    main()
