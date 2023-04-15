from chatscript.Conversation import Conversation
from chatscript.OpenAIClient import OpenAIClient


client = OpenAIClient()
convo = Conversation("search", client)

convo.system("""
Instructions:
- You are a research assistant.
- Your task is to help the user discover and summarize information.
- If you already know the information requested by the uesr, then respond with "ANSWER:" followed by the information.
- If you are unsure if you know the information requested by the user, then respond with "QUERY:" followed by an internet search query in order to find the information.
- If your previous message began with "QUERY:", then answer the next message with "RESULT:" followed by the result of the internet search.
- If your previous message began with "RESULT:", then answer the next message with "SUMMARY:" followed by a short summary of the most important pieces of information.
""")

convo.user("""
Which country has the largest population?
""")

convo.assistant("""
ANSWER: China has the largest population.
""")

convo.user("""
How many plants are in China?
""")


# should probably begin with "QUERY:"
convo.assistant()

convo.assistant(content="""
RESULT: China has over 39,000 vascular plants, including angiosperms, gymnosperms, ferns (monilophytes) and fern allies (lycophytes). Approximately 31,500 of these being native and over 50% being endemic. The vascular plants of China have been documented extensively in the Flora of China (series).
""")

# should begin with "SUMMARY:"
convo.assistant()

convo.user("""
What is the most popular Chinese plant?
""")
           
convo.assistant()

convo.assistant("""
Broad bean. Broad bean (Vicia faba) is a fruit-bearing flowering plant related to the pea. ...
Golden pothos. ...
Indian Lotus. ...
Chinese evergreen. ...
Snake plant. ...
Swiss cheese plant. ...
Bigleaf hydrangea. ...
Common hop.
""")

convo.assistant()

convo.save()
convo.write()
