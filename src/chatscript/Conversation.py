from os import path
import json
from chatscript.OpenAIClient import OpenAIClient


"""
# Types

```
Model = {
  'messages': list[Message]
}

type Message = { 
  'role': Role, 
  'content': str
}

type Role = "user" | "assistant" | "system"
```
"""


class Conversation:
    # - model: Model
    # - ix: int

    def __init__(self,  name: str, client: OpenAIClient):
        self.client = client
        self.name = name
        self.model = loadModel(self.name)
        self.focusIx = 0

    def __set_messages(self, messages):
        self.model['messages'] = messages

    messages = property(lambda self: self.model['messages'], __set_messages)

    def __getPreviousMessages(self):  # list[Message]
        return self.messages[:self.focusIx]

    def __getFocussedMessage(self):  # Message | None
        return index_list(self.messages, self.focusIx)

    def __pruneFromFocus(self):
        # Prune all messages from and including focus.
        # print(f"pruning from 0 up to (no including) {str(self.focusIx)}")
        self.messages = self.messages[:self.focusIx]

    def user(self, content: str) -> str:
        return self.__message(user(content), overwrite=False)

    def system(self, content: str) -> str:
        return self.__message(system(content), overwrite=False)

    def assistant(self, content: str = None, overwrite=False) -> str:
        return self.__message(assistant(content), overwrite)

    def __message(self, msgNew: dict, overwrite: bool) -> str:

        # clean input
        if msgNew['content'] is not None:
            msgNew['content'] = msgNew['content'].strip()

        # Apply update to focussed message if necessary.
        # - msgNew: Message
        # - overwrite: bool

        def update():
            # Force update of focussed message, which requires pruning any old
            # messages after focus.
            self.__pruneFromFocus()
            self.messages.append(msgNew)

            if msgNew['role'] == "assistant" and msgNew['content'] == None:
                # for an assistant message that has no explicit content, need to
                # query backend using messages up to but not including focus in
                # order to fill content
                msgResult = self.client.query(
                    self.__getPreviousMessages())

                self.messages[-1] = msgResult

        msgOld = self.__getFocussedMessage()

        if overwrite:
            # explicit overwrite, so update
            update()

        elif msgOld is None:
            # there is no old message, so update
            update()

        elif msgOld['role'] != msgNew['role']:
            # messages aren't even of the same role, so they aren't comparable,
            # so update
            update()

        else:
            # msgOld is not None
            role = msgOld['role']

            if role == "user" or role == "system":
                if msgOld['content'] != msgNew['content']:
                    # both messages are user-provided but have differing
                    # content, so need to update
                    update()
            elif role == "assistant":
                if msgOld['content'] is None:
                    # old content is None, so update
                    update()
                elif msgNew['content'] is not None and \
                        msgOld['content'] != msgNew['content']:
                    # both old and new content are non-None, and new content
                    # overwrites old content, so update
                    update()

        # increment focus
        self.focusIx += 1

        # if assistant message, then return content
        msgNew = self.messages[-1]
        if msgNew['role'] == 'assistant':
            return self.messages[-1]['content']
        else:
            return None

    def save(self): saveModel(self.name, self.model)

    def load(self): self.model = loadModel(self.name)

    def write(self): writeModel(self.name, self.model)


def emptyModel() -> dict:  # Model
    return {
        'messages': []
    }


def saveModel(name: str, model: dict):
    # - model: Model
    with open(jsonFilepath(name), "w+") as file:
        json.dump(model, file)


def loadModel(name: str) -> dict:  # Model
    # if no save exists, then first save an empty Model
    if not path.exists(jsonFilepath(name)):
        saveModel(name, emptyModel())

    with open(jsonFilepath(name), "r") as file:
        return json.load(file)


def writeModel(name: str, model: dict) -> dict:
    # Writes a pretty-printed version of model to a a markdown file.
    # - model: Model
    with open(mdFilepath(name), "w+") as file:
        for msg in model['messages']:
            file.write(f"# {msg['role']}\n\n{msg['content']}\n\n")


def jsonFilepath(name: str) -> str:
    return f"{name}.json"


def mdFilepath(name: str) -> str:
    return f"{name}.md"


def user(content: str) -> dict:  # Message
    return {'role': "user", 'content': content}


def assistant(content: str) -> dict:  # Message
    return {'role': "assistant", 'content': content}


def system(content: str) -> dict:  # Message
    return {'role': "system", 'content': content}


def index_dict(d: dict, k, default=None):
    # Safely indexes a dictionary
    # - d: dict[key, val]
    # - k: key
    # - default: val | None
    return d[k] if k in d else default


def index_list(l: list, i, default=None):
    # Safely indexes a list
    # - l: list[val]
    # - i: int
    # - default: val | None
    return l[i] if 0 <= i < len(l) else default
