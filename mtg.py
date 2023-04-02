from os import path
import json
from Conversation import *
from django.utils.text import slugify

n_card = 1
theme = "Lord Guillotine"

for _ in range(n_card):

    convo = Conversation("conversations/mtg")

    convo.system("""
You are an assistant for designing new Magic the Gathering cards based on prompts given by the user. Each card should have complicated and interesting mechanics that symbolize the essential aspects of the given theme. Each card should have a unique name that essence of the card. Make sure that each card is not over-powered. Make sure that each card's abilities are cohesive and straightforward. Each card should have short, creative, and thematic flavor text that is relevant to the flavor of the card's abilities and name. Respond to each prompt only exactly in this format:

card name
mana cost
card types
power/toughnes or NA
oracle text
""")

    convo.user(f"""
Design a new Magic the Gathering card based on {theme}.
""")

    card = convo.assistant(content=None)

    if True:
        card_lines = card.splitlines()
        card_data = {
            'theme': theme,
            'card name': card_lines[0].strip(),
            'mana cost': card_lines[1].strip(),
            'card types': card_lines[2].strip(),
            'power/toughness': card_lines[3].strip(),
            'oracle text': ("\n".join(map(lambda s: s.strip(), card_lines[3:]))).strip(),
        }

        filename = f"{slugify(card_data['card name'], allow_unicode=False)}"

        def makeFilepath(filename):
            return f"conversations/cards/{filename}.json"

        filepath = makeFilepath(filename)

        i = 0
        while path.exists(filepath):
            filepath = makeFilepath(f"{filename}_{i}")
            i += 1

        with open(filepath, "w+") as file:
            json.dump(card_data, file)
            print(f"created: {filepath}")
