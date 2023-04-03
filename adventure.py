from os import path
import json
from Conversation import *
from django.utils.text import slugify

"""
# Adventure

There are 3 lines of conversation:
  1. Master
    - system: You are the gamemaster for a text adventure game. The user
      (player) says what they do, and you respond with what happens next.
    - user: player actions
    - assistant: world actions
  2. Protagonist
    - system: You are a player of a text adventure game. You say what actiosn
      you take, and the user (gamemaster) responds with what happens next.
    - user: world actions
    - assistant: player actions
  3. Summarizer
    - system: You are a summarizer of a text adventure game history. The user
      gives the history of a text adventure game, and you respond with a short
      summary of it.
    - user: text adventure game history
    - assistant: summary of text adventure game
"""

# ==============================================================================
# [BEGIN] Config
# ==============================================================================

name = "alien-romantic"

directory_main = f"conversations/adventure/{name}/"

if not path.exists(directory_main):
    os.mkdir(directory_main)

filepath_history_json = f"{directory_main}game.json"

filepath_history_md = f"{directory_main}game.md"

init_summary = "Henry is a computer science PhD student who was in a relationship with a art student. You are an alien with highly advanced technology who is secretly visiting earth. No one knows that you are an alien. You have the ability to change your appearance at will to keep your identity secret, and to trick Henry into falling in love with you."

master_goal = "As the gamemaster, you goal is to write detailed and realistic descriptions of what should happen as a result of the the user's actions in the game. The user is trying to get into a romantic relationship with Henry, so include some obstacles the player's advances and other girls that could take away Henry's attention from the user. At some point in the game, there should be an alien attack."

player_goal = "As the player, your goal is to get into a romantic relationship with Henry without revealing your alien identity to anyone."

summary_bin = 6

rounds_count = 12

# ==============================================================================
# [END] Config
# ==============================================================================

"""
## Types

The 'items_old' are kept in storage, but aren't included in the prompts for generating the next items. The idea is that 'summary' summarizes everything in 'items_old', which compresses them and allows for the adventure to go on much longer. Though, there is loss of details over time.

History = {
  'items_old': HistoryItem[],
  'summary': str,
  'items': HistoryItem[]
}

HistoryItem = {
  'source': 'master' | 'player',
  'content': str
}
"""


def emptyHistory() -> dict:
    return {
        'items_old': [],
        'summary': init_summary,
        'items': []
    }


def showHistory(hist: dict) -> str:
    s = ""
    s += f"GAMEMASTER: {hist['summary']}\n\n"
    s += showHistoryItems(hist['items'])
    return s


def showHistoryItems(items: list) -> str:
    s = ""
    for item in items:
        if item['source'] == 'master':
            s += f"GAMEMASTER: {item['content']}\n\n"

        elif item['source'] == 'player':
            s += f"PLAYER: {item['content']}\n\n"
    return s


def markdownHistory(hist: dict) -> str:
    s = ""
    s += f"# GAMEMASTER (summary)\n\n{hist['summary']}\n\n"

    def markdownItem(item):
        nonlocal s
        if item['source'] == 'master':
            s += f"# GAMEMASTER\n\n{item['content']}\n\n"

        elif item['source'] == 'player':
            s += f"# PLAYER\n\n{item['content']}\n\n"
    
    for item in hist['items_old']:
        markdownItem(item)

    for item in hist['items']:
        markdownItem(item)

    return s


if not path.exists(filepath_history_json):
    with open(filepath_history_json, "w+") as file:
        json.dump(emptyHistory(), file)

with open(filepath_history_json, "r") as file:
    history = json.load(file)

master_title = "GAMEMASTER"
player_title = "PLAYER"

for _ in range(rounds_count):

    #
    # step 1: generate summary from history so far; batch summaries every
    # {summary_bin} messages
    #

    if len(history['items']) >= summary_bin:
        summarizer = Conversation("conversations/adventure/summarizer")
        # only summarize the items, since the new summary will be appended to the
        # old summary
        summarizer.system(f"""
You are a summarizer of text adventure game histories. The user will provide a history of a text adventure game, where the {player_title} says what they do and then the {master_title} says what happens as a consequence of their actions. You will respond with a short, couple-sentence summary of what happened in the text adventure game history. In your summary, make sure to focus heavily on the most important events, include introductions and details of important characters, and leave out the least important events.
    """)
        summarizer.user(f"""
The following is text adventure game history.

    {showHistoryItems(history['items'])}

    Write a short summary of what happened in this history.
    """)
        summary = summarizer.assistant()
        summarizer.save()
        history['summary'] = f"{history['summary']} {summary}"

        history['items_old'] = history['items_old'] + history['items']
        history['items'] = []

    #
    # step 2: get player action
    #
    player = Conversation(f"{directory_main}player")

    player.system(f"""
    You are the player of a text adventure game. As the player, you write from a first-person, active, present-tense perspective what you do next in the game. Then the user will respond with what happens next in the game as a consequence of your actions. And so on. Keep your responses within one or two paragraphs in length.

    {player_goal}
    """)
    # - source=master corresponds to user
    # - source=player corresponds to assistant
    player.user(history['summary'])
    for item in history['items']:
        if item['source'] == 'master':
            player.user(item['content'])
        if item['source'] == 'player':
            player.assistant(item['content'])

    player_content = player.assistant()
    player.save()

    history['items'].append({
        'source': 'player',
        'content': player_content
    })

    #
    # step 3: get consequence
    #

    master = Conversation(f"{directory_main}master")

    master.system(f"""
    You are the gamemaster of a text adventure game. The user will write what they do in the game from first-person perspective. You should respond to the user with a description of what happens next in the game as a result of the player's actions, and then ask the player what they want to do next. Keep your responses within one or two paragraphs in length.

    {master_goal}
    """)
    # - source=master corresponds to assistant
    # - source=player corresponds to user
    master.assistant(history['summary'])
    for item in history['items']:
        if item['source'] == 'master':
            master.assistant(item['content'])
        if item['source'] == 'player':
            master.user(item['content'])

    master_content = master.assistant()

    master.save()

    history['items'].append({
        'source': 'master',
        'content': master_content
    })

    #
    # step 4: save and write
    #

    with open(filepath_history_json, "w") as file:
        json.dump(history, file)

    with open(filepath_history_md, "w+") as file:
        file.write(markdownHistory(history))
