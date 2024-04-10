import json
from src.testing.check_asserts import check_asserts


import subprocess
import json


# Run prospector via cli on a given file that is given as parameter
# The output structure is as follows:
def run_prospector(file_path):
    command = f"python -m prospector {file_path} -o json --zero-exit"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return True, None
    print("raw output", result)
    output = json.loads(result.stdout.strip())
    print(output["summary"]["message_count"], "issues found in", file_path)
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
    command = f"crosshair check {file_path} --analysis_kind asserts"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    returncode = result.returncode
    print("crosshair exit code", result.returncode)
    output = result.stdout.strip()
    print("crosshair output", output)
    output = parse_mypy_output(output)

    # if output is a list and empty and returncode is 1, rais exception
    if returncode == 1 and len(output) == 0:
        return False, "Verification failed. No issues triagable by Crosshair found."
    elif returncode == 0:
        return True, None
    return False, output
