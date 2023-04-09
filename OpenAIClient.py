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
        if not path.exists(config_filepath):
            print(f"""
[OpenAIClient] The OpenAI config file {config_filepath} does not exist. You must create a config file with this name with the following default template:
```
{{
    "api_key": "<<your OpenAI API key>>",
    "organization_id": "<<optionally, your OpenAI organization id>>",
    "model": "gpt-3.5-turbo"
}}
```
""".strip())
            raise Exception(f"config file not found: {config_filepath}")

        self.setConfig(json.load(open(config_filepath, "r")))

    def setConfig(self, config):
        self.config = config
        openai.api_key = self.config['api_key']
        if 'organization_id' in self.config:
            openai.organization = self.config['organization_id']
        if not 'model' in self.config:
            self.config['model'] = "gpt-3.5-turbo"

    def query(self, messages):  # -> Message
        # messages: list[Message]

        print("query ...")

        result = openai.ChatCompletion.create(
            model=self.config['model'],
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


OpenAIClient.instance = OpenAIClient()
