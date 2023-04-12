from os import path
import json
from Conversation import *


convo = Conversation("conversations/poem")

convo.system("""
You are an assistant for writing Pulitzer-prize winning sonnets. The user will give a prompt specifying exactly what the poem should be about, and you will reply with an excellent poem that satisfies all of the specifications.
""")

convo.user("""
Write a sonnet poem about the mechanical design for an automatic shower machine built with a Raspberry Pi and small motors. Use fancy, technical, scientific, and poetic yet easy-to-understand language. The sonnet should rhyme. The sonnet should use weave in the idea that the night is beautiful because the light is more visible in the dark.
""")

convo.assistant()
convo.save()
convo.write()
