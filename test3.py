import os
from os import path
import sys
import json
import openai

openai_config = json.load(open("openai.json", "r+"))
openai.api_key = openai_config["api_key"]
openai.organization = openai_config["organization_id"]

# Conversation

# Value = { case: 'Query', message: Message | None }
#       | { case: 'Message', message: Message }
# Message = { role: String, content: String }


def query(messages):
    print("[>] query sent ...")
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print("[>] query answered ✓")
    try:
        choice = result['choices'][0]
    except IndexError:
        print("response with node choices")

    if choice['finish_reason'] != "stop":
        raise Exception(f"finish reason: {choice['finish_reason']}")

    print("[>] query is valid ✓")
    message = choice['message']

    if False:
        print(40 * "=")
        print(message['content'])
        print(40 * "=")

    return message


class Conversation:
    # ident: String
    # values: List<Value>
    def __init__(self, ident, values):
        self.ident = ident
        self.values = values

    # update according to diff between current values and given values
    #
    # values: List<Value>
    def update(self, values):
        valuesNext = []
        for i in range(len(values)):
            if len(self.values) < i + 1:
                # no more old values left, so just add new values
                valuesNext += values[i:]
                break

            valueOld = self.values[i]
            valueNew = values[i]
            if 'overwrite' in valueNew and valueNew['overwrite']:
                # overwrite the old query
                valuesNext.append(valueNew)
                continue
            if not valueOld['case'] == valueNew['case']:
                # value mismatch, so overwrite rest of values
                valuesNext += values[i:]
                break
            elif valueNew['case'] == 'Message':
                if valueOld['message']['content'] == valueNew['message']['content']:
                    # match
                    valuesNext.append(valueOld)
                    continue
                else:
                    # message mismatch, so use new values from here
                    valuesNext += values[i:]
                    break
            elif valueNew['case'] == 'Query':
                if valueNew['message'] is None:
                    # just keep the current query message if new value doesn't explicitly overwrite it
                    valuesNext.append(valueOld)
                    continue
                else:
                    # overwrite the old query
                    valuesNext.append(valueNew)
                    continue

        self.values = valuesNext

    # generates the messages of each Query value that has a None message
    def submit(self):
        messages = []
        for value in self.values:
            if value['case'] == 'Message':
                # record message
                messages.append(value['message'])
            elif value['case'] == 'Query':
                if value['message'] is None:
                    # fill in query
                    message = query(messages)
                    value['message'] = message
                else:
                    # already filled
                    messages.append(value['message'])
            else:
                raise Exception(f"invalid value case: {value['case']}")

    def read(): pass

    def write(self, file):
        def writeMessage(message):
            if message['role'] == 'user':
                file.write(
                    f"====[ USER ]=================================================================\n\n")
                file.write(f"{message['content']}\n\n")
            elif message['role'] == 'system':
                file.write(
                    f"============================================================[ SYSTEM ]=======\n\n")
                file.write(f"{message['content']}\n\n")
            elif message['role'] == 'assistant':
                file.write(
                    f"============================================================[ ASSISTANT ]====\n\n")
                file.write(f"{message['content']}\n\n")

        for value in self.values:
            if value['case'] == 'Message':
                writeMessage(value['message'])
            elif value['case'] == 'Query':
                if value['message'] is None:
                    file.write("[unevaluated query]\n\n")
                else:
                    writeMessage(value['message'])
            else:
                raise Exception(f"invalid value case: {value['case']}")

    def print(self):
        for value in self.values:
            if value['case'] == 'Message':
                print(f"\n#ROLE {value['message']['role']}\n")
                print(value['message']['content'])
            elif value['case'] == 'Query':
                if value['message'] is None:
                    print("\nEMPTY\n")
                else:
                    print(f"\n#ROLE {value['message']['role']}\n")
                    print(value['message']['content'])
            else:
                raise Exception(f"invalid value case: {value['case']}")

    def load(file):
        return Conversation.fromJSON(json.load(file))

    def save(self, file):
        json.dump(self.toJSON(), file)

    def toJSON(self):
        return {
            'ident': self.ident,
            'values': self.values
        }

    def fromJSON(obj):
        ident = obj['ident']
        values = obj['values']
        return Conversation(ident, values)


def system(content):
    return {
        'case': 'Message',
        'message': {
            'role': 'system',
            'content': content
        }
    }


def user(content):
    return {
        'case': 'Message',
        'message': {
            'role': 'user',
            'content': content
        }
    }


def assistant(content=None, overwrite=False):
    if content is None:
        return {
            'case': 'Query',
            'message': None,
            'overwrite': overwrite
        }
    else:
        return {
            'case': 'Query',
            'message': {
                'role': 'assistant',
                'content': content
            },
            'overwrite': overwrite
        }


def shortstory(ident, genre, theme, main_idea, author):
    filepath = f"conversations/shortstory/{ident}.json"
    filepath_output = f"conversations/shortstory/{ident}.md"

    # create an empty Conversation at the filepath if doesn't already exist
    if not path.exists(filepath):
        convo = Conversation(ident, [])
        convo.save(open(filepath, "w+"))

    convo = Conversation.load(open(filepath, "r+"))

    convo.update([
        system(
            "You are a creative and knowledgeable writing assistant for a short story author. The author wants to write innovative, unique, original stories that appeal to niche audiences and not necessarily to the general public."
        ),
        user(
            f"I am writing a {genre} short story with this theme: {theme}. Write a list of interesting, original, and thematic ideas that would be interesting to include in my short story."
        ),
        assistant(None),
        user(
            "Write a brief summary of a short story that ties together a few of the ideas that you listed above. The summary should include a description of the setting, an introduction to the main characters, the main plot points, and a conclusion."
        ),
        assistant(None),
        user(
            f"Write a revised version of that summary which uses most of the same details, but also makes sure to include this main idea: {main_idea}."
        ),
        assistant(None),
        user(
            f"Write a short story in the style of {author} and based on that summary. Make sure the story is around 2500 words. The story should first introduce the setting and main characters, then flush out the details of and transition smoothly between all the plot points, and then finish the story with the conclusion."
        ),
        assistant(None),
        user(
            "Write a revised version of that short story. Use more stylized language with vivid descriptions and a few metaphors, include more unique details about the setting and characters, and use dialogue more frequently. Make the revised story under 2000 words."
        ),
        assistant(None),
    ])
    convo.submit()

    convo.write(open(filepath_output, "w+"))
    convo.save(open(filepath, "w+"))


shortstory(
    "test3-moon",
    genre="science fiction",
    theme="in a near-term future where many civilians live and work on the moon, a top secret spy operation is conducted in an international lunar colony",
    main_idea="political intrigue between spies of different nation-companies that are vying for influence in the lunar colony",
    author="Isaac Asimov"
)
