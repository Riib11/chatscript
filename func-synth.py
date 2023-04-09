from os import path
import json
from Conversation import *
import ast


def f(x):
    return x * x


domain = range(0, 6 + 1, 2)

convo = Conversation("conversations/func-synth")

convo.system("""
You are helping a programmer write a Python function given only the expected inputs and outputs of that function. Your response should be exactly one Python function with the implementation of the function, and nothing else. Do not include any explanation in your reponse.
""")

examples = ""
for x in domain:
    examples += f"f({x}) = {f(x)}\n"

convo.user(f"""
`fql` is a function that inputs a number and outputs a number. The following are examples of the behavior of `fql`:

```
{examples}
```

Write a Python function `fql` that has this behavior.
""")

response = convo.assistant()


# parse as function definition
# parsed_mdl = ast.parse(response, mode='eval')
# print(ast.dump(parsed_mdl))

convo.save()
convo.write()
