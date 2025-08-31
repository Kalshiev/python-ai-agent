import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python, run_python
from functions.write_file_content import schema_write_file_content, write_file_content

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_run_python, schema_write_file_content
    ]
)

def main():
    if len(sys.argv) < 2:
        print("Please provide a prompt as a command line argument.")
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=sys.argv[1])])]

    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                system_instruction=system_prompt)
            )

            for candidate in response.candidates:
                messages.append(candidate.content)

            if response.function_calls:
                for function_call_part in response.function_calls:

                    function_call_result = call_function(function_call_part)

                    messages.append(function_call_result)
                continue
            
            if response.text:
                print(response.text)
                break
                

                    #if function_call_result.parts[0].function_response.response is not None and "--verbose" in sys.argv:
                        #print(f"-> {function_call_result.parts[0].function_response.response}")
                    #elif function_call_result.parts[0].function_response.error is None and function_call_result.parts[0].function_response.response is None:
                        #raise Exception("Fatal error occurred")

        except Exception as e:
            print(f"Error occurred: {e}")


    if "--verbose" in sys.argv:
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def call_function(function_call_part, verbose=False):

    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name == "get_files_info":
        function_result = get_files_info(**args)
        function_name = "get_files_info"
    elif function_call_part.name == "get_file_content":
        function_result = get_file_content(**args)
        function_name = "get_file_content"
    elif function_call_part.name == "run_python":
        function_result = run_python(**args)
        function_name = "run_python"
    elif function_call_part.name == "write_file_content":
        function_result = write_file_content(**args)
        function_name = "write_file_content"
    else:
        function_name = function_call_part.name
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)
if __name__ == "__main__":
    main()
