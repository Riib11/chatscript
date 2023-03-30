import os
from os import path
import pickle
import sys
import json
from Conversation import *

store = {}

convo1 = Conversation("conversations/test1")

convo1.system("""
You are an assistant for designing new Magic the Gathering cards based on prompts given by the user. Each card you design should have mechanics that symbolize some essential aspects of the theme. Respond to each prompt exactly in the following format:

- card name
- mana cost
- card types
- oracle text
- power and toughnes (if the card is a creature)
""")

theme = "Ayn Rand"

convo1.user(f"""
"Design a new Magic the Gathering card based on {theme}.
""")

convo1.assistant(content=None, store=store, key="card1")

convo1.save()
convo1.write()

print("store", store)