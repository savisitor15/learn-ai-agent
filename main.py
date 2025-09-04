import os
import sys
import logging as log
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEMPROMPT
from config import MAX_ITER
from call_functions import available_functions
from call_function import call_function


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
    load_dotenv()
    level = log.INFO
    if len(sys.argv) < 2:
        sys.argv.append("run tests.py")
    
    arguments = initArgs().parse_args()
    if arguments.verbose:
        level = log.DEBUG
    logger = loggerInit(log.getLogger(), level)
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    input_loop(client, arguments.prompt, arguments.verbose)
    


def input_loop(client: genai.Client, initial_prompt, verbose=False):
    prompt = initial_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=initial_prompt)]),
                ]
    log.debug(f"Intial user prompt: {initial_prompt}")
    iPrompts = 1
    while True:
        iPrompts += 1
        if iPrompts > MAX_ITER:
            log.info("Maximum prompts reached")
            sys.exit(1)
        try:
            log.debug(f"User prompt: {prompt}")
            final_response = generate_contents(client, messages, verbose)
            if final_response:
                log.info("Final response")
                log.info(final_response)
                break
        except Exception as e:
            print(f"Error in generate_contents: {e}")
    

def generate_contents(client: genai.Client, messages, verbose=False):
    
    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEMPROMPT
        ),
        )
    log.debug(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
    log.debug(f"Response tokens: {resp.usage_metadata.candidates_token_count}")
    if resp.candidates:
        for candidate in resp.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)
    if not resp.function_calls:
        return resp.text
    function_responses = []
    for function_call_part in resp.function_calls:
        log.info(f"Calling function: {function_call_part.name}({function_call_part.args})")
        # call the function
        function_call_result = call_function(function_call_part, verbose)

        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise ValueError("Empty function response")
        log.debug(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    if not function_responses:
        raise Exception("no function responses generated")
    messages.append(types.Content(role="user", parts=function_responses))



if __name__ == "__main__":
    main()

