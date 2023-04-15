from chatscript.OpenAIClient import OpenAIClient
from chatscript.Conversation import Conversation

client = OpenAIClient()
convo = Conversation("world_desc", client)
convo.system("""
Instructions:
- You are an erudite storyteller and worldbuilder.
- Your task is to create interesting and complex descriptions of fantasy worlds for an RPG.
- The user will give a prompt to base the world on.
- You should respond with a dense, descriptive, detailed, concise introduction to a fantasy world based on the user's prompt.
""")

convo.user("""
Write an introduction to a fantasy world about time traveling lawers in New York City, where time travel is not well understood and people must use it very carefully and only for very short temporal distances (except for emergencies perhaps).
""")
convo.assistant()

short_desc = "a government official"
convo.user(f"""
Write a paragraph description of {short_desc} who lives in this world.
""")
convo.assistant()

convo.save()
convo.write()