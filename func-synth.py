from os import path
import json
from Conversation import *
import ast
import subprocess
import csv


# Inputs

script_name = "func-synth"


function_name = "foo"

domain = range(0, 10, 1)

spec_function = "2*x + 2"


def spec(x):
    return eval(spec_function, {}, {"x": x})


# Conversation

# clear logfile if it exists
log_filename = f"conversations/{script_name}/{spec_function}.txt"
if path.exists(log_filename):
    with open(log_filename, "w") as file:
        file.write("")


convo = Conversation(f"conversations/{script_name}")

convo.system("""
You are helping a programmer write a Python function given only the expected inputs and outputs of that function. Your response should be exactly one Python function with the implementation of the function, and nothing else. Do not include any explanation in your reponse.

The function should only use integer addition, subtraction, and multiplication. It should not use any other operations.
""")

examples = ""
for x in domain:
    examples += f"{function_name}({x}) = {spec(x)}\n"

convo.user(f"""
`{function_name}` is a function that inputs a number and outputs a number. The following are examples of the expected inputs and outputs of `{function_name}`:

```
{examples}
```

Write a Python function `{function_name}` that has this behavior.
""")
           


# until success, which breaks
while True:

    response = convo.assistant(overwrite=True)

    convo.save()
    convo.write()

    # interpret response as function definition
    # try to parse it, and report error if fails to parse
    try:
        ast.parse(response)
    except Exception as e:
        # !TODO is it useful to print this error to assistant?
        print(f"syntax error: {e}")
        convo.user(f"""
Your program has a syntax error:

{e}

Rewrite your function and make sure to not have any syntax errors.
""")
        continue

    # if successfully parse
    function_def = response.strip(" `")

    if not path.exists(log_filename):
        # initialize
        with open(log_filename, "w+") as file:
            file.write(f"goal function: {spec_function}\n\n")
    with open(log_filename, "a") as file:
        # append attempt
        file.write(f"{function_def}\n\n")

    # write a python program that includes the function defined by the response,
    # and writes the outputs of that function as applied to each element of the
    # domain.
    tmp_name = f"{script_name}-tmp"
    indented_newline = "\n    "
    with open(f"{tmp_name}.py", "w+") as file:

        file.write(f"""
import csv

{function_def}

domain = {domain}

with open("{tmp_name}.csv", "w+") as file:
    w = csv.writer(file)
    for x in domain:
        w.writerow([x, {function_name}(x)])
""".strip())

    # run that python program to generate the input/output data
    subprocess.run(["python3", f"{tmp_name}.py"])

    errors = []
    errors_str = ""
    with open(f"{tmp_name}.csv", "r") as file:
        r = csv.reader(file)
        for row in r:
            x = int(row[0])
            y = int(row[1])
            y_correct = spec(x)
            if y != y_correct:
                errors.append([x, y])
                errors_str += f"expected {function_name}({x}) = {y_correct}, but your implementation has {function_name}({x}) = {y}."

    if len(errors) == 0:
        print("SUCCESS")
        break  # success!
    else:
        comma = ", "
        print(f"FAILURE: {comma.join(map(str, errors))}")
        convo.user(f"""
Your implementation has these incorrect outputs: {errors_str}.

Write a more correct version of {function_name} that does not result in these incorrect outputs.
""")
