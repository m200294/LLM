import json
import sys
import argparse
import os
from dotenv import load_dotenv
from tools import available_tools, call_function
from config import MAX_LOOP

# OpenAI is a class we use to communicate with the LLM
from openai import OpenAI
from prompt import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("API key not found cuh")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    # creating user input
    parser = argparse.ArgumentParser(description="user prompt via input")

    # arg_1
    parser.add_argument(
        "user_prompt",
        type=str,
        help="Add a string while running the program, this will serve as the user prompt",
    )

    # arg_2 (optional --)
    parser.add_argument(
        "--verbose", action="store_true", help="This will Enable verbosity init"
    )

    user_input = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input.user_prompt},
    ]

    if user_input.verbose:
        print(f"User prompt: {user_input.user_prompt}")

    for calls in range(MAX_LOOP):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_tools,
        )
        message = response.choices[0].message
        messages.append(message)

        if response.usage is None:
            raise RuntimeError("The API request done did failed")

        if user_input.verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, user_input.verbose)
                # print(f"Calling function: {tool_call.function.name}({function_args})")
                if not result_message["content"]:
                    raise Exception(
                        f"Twin Nothing returned from {tool_call.function.name}"
                    )
                messages.append(result_message)
                if user_input.verbose:
                    print(f"-> {result_message['content']}")
        else:
            return print(f"Response:\n {message.content}")

    print(f"Error: agent hit the {MAX_LOOP}-iteration limit without a final response")
    sys.exit(1)


if __name__ == "__main__":
    main()
