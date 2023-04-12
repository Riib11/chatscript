import os
from os import path
import pickle
import sys
import json
from OpenAIClient import OpenAIClient

client = OpenAIClient()


def index(d, k, default=None):
    # Safely indexes a dictionary
    # - d: Dict<key, val>
    # - k: key
    # - default: val | None
    return d[k] if k in d else default


class Item:
    # def __init__(self, role, store, content, key):
    def __init__(self, args):
        self.role = args['role']
        self.store = args['store']
        self.content = args['content']
        self.key = index(args, 'key', default=None)

    # returns whether or not the item was updated
    def update(self, item):
        raise Exception("Item.update is abstract")

    def show(self):
        raise Exception("Item.show is abstract")

    def updateStore(self):
        if self.key is None:
            return
        self.store[self.key] = self.content

    def toJSON(self):
        return {'role': self.role, 'content': self.content}


class SystemItem(Item):
    def __init__(self, store, content, **kwargs):
        args = {
            'role': "system",
            'content': content,
            'store': store,
        }
        if 'key' in kwargs:
            args['key'] = kwargs['key']
        super().__init__(args)

    def update(self, item):
        if item.content != self.content:
            self.content = item.content
            return True
        return False

    def show(self):
        return f"# SYSTEM\n\n{self.content}\n\n"

    def toJSON(self):
        return {'role': self.role, 'content': self.content}


class UserItem(Item):
    def __init__(self, store, content, **kwargs):
        args = {
            'role': "user",
            'content': content,
            'store': store,
        }
        if 'key' in kwargs:
            args['key'] = kwargs['key']
        super().__init__(args)

    def update(self, item):
        if item.content != self.content:
            self.content = item.content
            return True
        return False

    def show(self):
        return f"# USER\n\n{self.content}\n\n"


class AssistantItem(Item):
    def __init__(self, store, key=None, content=None, **kwargs):
        args = {
            'role': "assistant",
            'content': content,
            'store': store,
        }
        if 'key' in kwargs:
            args['key'] = kwargs['key']
        super().__init__(args)

    def update(self, item):
        # ignore None-content updates
        if item.content is None:
            pass
        elif self.content != item.content:
            self.content = item.content
            return True

    def show(self):
        if self.content is None:
            return f"# ASSISTANT\n\n<not yet generated>\n\n"
        else:
            return f"# ASSISTANT\n\n{self.content}\n\n"

    def toJSON(self):
        raise Exception(
            "should not try to Item.toJSON on an assistant Item that hasn't been computed yet")


class Conversation:
    # dir: String (directory path)
    # ident: String
    # items: Array<Item>
    # store: Dict<String, Any>

    def __init__(self, store, items):
        self.store = store
        self.items = items

    def Empty(): return Conversation({}, [])

    def interact(filepath, items):
        convo = Conversation.load(filepath)
        convo.update(items)
        convo.write(filepath)
        convo.save(filepath)

    def update(self, items):
        for i in range(min(len(self.items), len(items))):
            itemOld = self.items[i]
            itemNew = items[i]
            isUpdated = itemOld.update(itemNew)
            # if updated, then just replace the rest of the old items with the
            # rest of the new items
            if isUpdated:
                self.items = self.items[:i+1] + items[i+1:]
                return True
        # # if the new items list is longer (or same length) as old items, then
        # # append the rest of new items (if any)
        # if len(self.items) <= len(items):
        #     self.items = self.items[:i+1] + items[i+1:]
        # # if the new items is shorter, then prune any extra old items
        # else:
        #     self.items = self.items[:i+1]
        self.items = self.items[:i+1] + items[i+1:]

    def submit(self):
        messages = []
        for item in self.items:
            if isinstance(item, AssistantItem):
                message = client.query(messages)
                messages.append(message)
                self.items.apend(AssistantItem(self.store, item.key, None))
            self.messages.append(item.toJSON())

    def save(self, filepath):
        filepath_pickel = filepath + ".pickel"
        pickle.dump(self, open(filepath_pickel, 'x+'))

    def load(filepath):
        filepath_pickel = filepath + ".pickel"
        # if filepath does not exist, then save an empty Conversation there
        # first
        if not path.exists(filepath_pickel):
            Conversation.Empty().save(filepath_pickel)
        return pickle.load(open(filepath_pickel, 'r'))

    def write(self, filepath):
        filepath_md = filepath + ".md"
        with open(filepath_md, '+') as file:
            for item in self.items:
                file.write(item.show())

    def toJSON(self):
        # returns JOSN for list of messages
        messages = []
        for item in self.items:
            messages.push(item.toJSON())
        return messages
