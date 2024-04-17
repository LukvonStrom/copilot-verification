import json
import os
from src.testing.check_asserts import check_asserts


import subprocess
import json


# Run prospector via cli on a given file that is given as parameter
# The output structure is as follows:
def run_prospector(file_path):


    # find .prospector.yaml in the root dir
    prospector_config_path = os.path.join(os.getcwd(), ".prospector.yaml")
    # print(prospector_config_path)

    # print("-"*500)
    command = f"python -m prospector --profile {prospector_config_path} --zero-exit {file_path}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # print("raw output", result)

    # print('-'*500)
    if result.returncode == 0:
        try:
            output = json.loads(result.stdout.strip())
        except Exception:
            output = result.stdout.strip()
    else:
        try:
            output = json.loads(result.stderr.strip())
        except Exception:
            output = result.stderr.strip()
    # print(output["summary"]["message_count"], "issues found in", file_path)
    if result.returncode == 0:
        return True, output
    return False, output


# write a mypy parser from a string, split by newline then parse: {FILENAME}:{LINE_NUMBER}: error: {MESSAGE}
def parse_mypy_output(output):
    lines = output.split("\n")
    errors = []
    for line in lines:
        if "error" in line:
            parts = line.split(":")
            message = parts[3:]
            errors.append(
                {
                    "line_number": parts[1],
                    "message": (("".join(message)).strip()).replace("  ", " "),
                }
            )
    return errors


# write a method that parses a targetfile with ast and checks if there are any asserts statements
# run crosshair via crosshair check {FILENAME} --analysis_kind asserts
def run_crosshair(file_path):

    if not check_asserts(file_path):
        # throw exception
        return False, f"No asserts found"
    command = f"python -m crosshair check {file_path} --analysis_kind asserts"
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
    returncode = result.returncode
    # print("crosshair exit code", result.returncode)

    # print('-'*1000)
    # print("running", command, "yielded", result, "with", result.stdout)
    # print('-'*1000)
    if returncode == 0:
        output = result.stdout.strip()
    else:
        output = result.stderr.strip()
    print("crosshair output", output)
    output = parse_mypy_output(output)

    # if output is a list and empty and returncode is 1, rais exception
    if returncode == 1 and len(output) == 0:
        return False, "Verification failed. No issues triagable by Crosshair found."
    elif returncode == 0:
        return True, None
    return False, output
