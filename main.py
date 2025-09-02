import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import logging as log
import argparse
from prompts import SYSTEMPROMPT
from call_functions import available_functions


def initArgs() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="Boot dev - AI Agent", description="A simple ai agent using Google")
    parser.add_argument("prompt", help="Store the user input prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    return parser


def loggerInit(logger : log.Logger, level: int) -> log.Logger:
    if log.getLevelName(level).startswith("Level"):
        raise ValueError("Invalid log level!")
    logger.setLevel(level)
    return logger


def main():
    system_prompt = SYSTEMPROMPT
    level = log.INFO
    
    arguments = initArgs().parse_args()
    if arguments.verbose:
        level = log.DEBUG
    logger = loggerInit(log.getLogger(), level)
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = arguments.prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),
                ]
    # content = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    generate_contents(client, messages)
    log.debug(f"User prompt: {arguments.prompt}")
    

def generate_contents(client, messages):
    
    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEMPROMPT
        ),
        )
    if (resp.function_calls != None):
        for function_call_part in resp.function_calls:
            log.info(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        log.info(resp.text)
    log.debug(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
    log.debug(f"Response tokens: {resp.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()

