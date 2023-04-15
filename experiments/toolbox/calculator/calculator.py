from chatscript.Conversation import Conversation
from chatscript.OpenAIClient import OpenAIClient


"""
The AI can make requests to the calculator interface.

The calculator responds with an ASSISTANT message of the form
```
ASSISTANT
CALCULATOR: <input> = <output>
```

"""

client = OpenAIClient()
convo = Conversation("calculator", client)

convo.system("""
You are an arithmetic assistant.
""")

convo.user("""
Question: Let $n$ be the average of $1, 2, 3$. Let $m$ be the average of $4, 5, 6$. What is $m + n$?

Break the answer to this question into a sequence of basic arithmetic operations that use only addition and multiplication.
""")

convo.assistant()

convo.save()
convo.write()
