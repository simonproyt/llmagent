

from google.genai import types 
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content 
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file]
)


def call_function(function_call, verbose=False):
    """Call one of the available helper functions and return a types.Content result.

    Args:
        function_call: a types.FunctionCall with .name and .args
        verbose: if True, print full name+args; otherwise print a short line

    Returns:
        types.Content containing a single Part.from_function_response with the
        function result placed under the "result" key (or an error dict).
    """
    function_name = function_call.name or ""

    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}
    # Ensure the working directory is the calculator app
    args["working_directory"] = "./calculator"

    # Call the actual function and capture its result
    try:
        function_result = function_map[function_name](**args)
    except Exception as e:
        function_result = f"Error: exception when calling function: {e}"

    # Provide both a structured function response (for tooling) and a plain-text
    # part so the model can *read* the results in the next iteration.
    import json
    try:
        result_text = json.dumps(function_result, default=str)
    except Exception:
        result_text = str(function_result)

    # Wrap the (string or dict-like) result into a response dict and include a
    # human-readable text part to ensure the model sees file names / content.
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            ),
            types.Part(text=result_text),
        ],
    )
