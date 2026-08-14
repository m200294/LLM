import argparse
import os
from dotenv import load_dotenv

# OpenAI is a class we use to communicate with the LLM
from openai import OpenAI


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

    messages = [{"role": "user", "content": user_input.user_prompt}]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )
    if response.usage is None:
        raise RuntimeError("The API request done did failed")

    if user_input.verbose:
        print(f"User prompt: {user_input.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
