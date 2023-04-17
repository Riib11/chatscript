"""
Summarizes a text document into roughly a single paragraph.
The summary will be logged to the console.
"""

from Conversation import *

text = """
TEXT TO SUMMARIZE
"""

convo = Conversation("summary")

convo.system(f"""
TLDR summarization is a form of summarization for information-dense text documents. TLDR summarization involves high source compression, removes stop words and summarizes the document whilst retaining the most important meaning. The result is a TLDR summary, which is a short summary that retains all of the meaning and context of the original document.

You are an assistant that performs TLDR summarization. The user will provide a text document, and you should reply with just the TLDR summary of that text document.
""")

convo.user(text)

result = convo.assistant()
convo.save()
print(result)
