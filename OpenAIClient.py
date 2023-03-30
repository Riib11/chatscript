import os
from os import path
import pickle
import sys
import json
import openai

# type Message = { 'role': Rule, 'content': String }
# type Rule = "User" | "Assistant" | "System"


class OpenAIClient:
    def __init__(self, config_filepath="openai.json"):
        self.setConfig(json.load(open(config_filepath, "r+")))

    def setConfig(self, config):
        self.config = config
        openai.api_key = self.config['api_key']
        openai.organization = self.config['organization_id']

    def query(self, messages):  # -> Message
        # messages: list[Message]

        print("query ...")

        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        print("query ✓")

        try:
            choice = result['choices'][0]
        except IndexError:
            raise Exception(f"response had no choices")

        if choice['finish_reason'] != "stop":
            raise Exception(f"finish reason: {choice['finish_reason']}")

        message = choice['message']
        message['content'] = message['content'].strip()

        if True:
            print("==[ response ]==================================================")
            print(message['content'])
            print("================================================================")

        print()

        return message


client = OpenAIClient()
