from google.genai import types
from call_functions import functions_defined
from config import WORKING_DIR


def call_function(function_call_part: types.FunctionCall, verbose=False) -> types.Content:

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_name = function_call_part.name
    function_called = functions_defined.get(function_name)
    if not function_called:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
        )
    function_result = function_called(WORKING_DIR, **function_call_part.args)
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)

