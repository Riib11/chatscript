# chatscript (Python)

This project provides a simple python interface to writing __chatscripts__ for
generating sequences of calls to OpenAI's GPT chat API. A __chatscript__ is an
imperative script (this project provides an interface to Python, but the same
interface generalizes to any imperative programming language) that can create
`Conversation` objects and make _message_ calls to it. 

```python
derivativebot = Conversation("derivativebot")
```

There are three kinds of messages: `user`, `system`, and `assistant`. The
following script show how to use these messages together in a simple script.

```python
from os import path

"""
# derivativebot

This program defines a chatscript for asking for the derivatives and 
explanations of how to take the derivatives of a collection of user-specified 
functions. The results are written to {answers_filepath}.
"""

answers_filepath = "derivatives.md"

functions = [
  "12",
  "2 x^2",
  "e^3",
  "10 log(x)"
]

if not path.exists(answers_filepath):
  with open(answers_filepath, "w+") as file:
    file.write("# Derivative Examples\n\n")


# A 'system' message corresponds to an initialization of the assistant that 
# tells it how to behave.
derivativebot.system("""
You are high school calculus tutor. Answer the user's questions will detailed step-by-step reasoning about how to take the derivative of a function. In your answer, first write the derivative of the user's function. Then on the next line after that, write a step-by-step explanation of how to calculate that derivative.
""")

for function in functions:
  # A 'user' message corresponds corresponds to a message from the user to the 
  # asssistant.
  derivativebot.user(f"What is the derivative {function}$?")
  # An 'assistant' message corresonds to a query to the GPT chat API.
  answer = derivativebot.assistant()

  # interprete the answer
  lines = answer.splitlines()
  derivative = lines[0].strip()
  explanation = "\n".join(lines[1:]).strip()

  with open(answers_filepath, "a+") as file:
    file.write(f"""
{function}
- derivative: {derivative}
- explanation: {explanation}

""")
```

## Installation

To install this project as a python module:

```
make install
```

## Organization

- `Conversation.py`: Defines the class `Conversation` which is the main
  interface to chatscripts provided by this project.
- `OpenAIClient.py`: Defines a simple wrapper class `OpenAIClient` for making
  calls to OpenAI's chat API. Exposes static instance `OpenAIClient.instances`.
- `conversations/`: some examples of histories and results from example
  chatscripts I've written.

## API Key

To make OpenAI API calls, you need to specify an OpenAI API
configuration. By default, looks for `openai.json`. The configuration file has
the following format:
```
{
    'api_key': '<<your OpenAI API key>>',
    'organization_id': '<<optionally, your OpenAI organization id>>'
}
```

## Usage Details

The module `Conversation.py` defines a class `Conversation` that corresponds to
a single line of conversation between you (the user) and the assistant. A
`Conversation` requires a name which lets it write to a file a _cache of results
of the previous run_. Whenever the chatscript is run, the messages generated
for sending to the chat API (at each `Conversation.assistant(...)` call) are
first compared to the cache of the previous state of the conversation. If none
of the messages _before_ this assistant message have changed, and there exists
an assistant response already in the cache, then the previous assistant response
is used for this run of the chatscript instead of the calling the chat API
again.

This can be very useful when tinkering with a chatscript. For example when you
run the script again after appending more messages to it, it won't re-query at
assistant calls before the new messages.

This behavior can be modified by some optional arguments to
`Conversation.assistant`:

```python
Conversation.assistant(
  self,
  # Explicitly specify content to overwrite the cached assistant response. If 
  # {content == None} then this yields an API call the response of which is 
  # returned by this function and written to the cache. If {content != None} 
  # then {content} is used as if it was the API response and no actual API call 
  # is made.
  content: str = None, 
  # Use {content} to overwrite the cached assistant response; if 
  # {content == None} then this result in an API call.
  overwrite = False 
)
```