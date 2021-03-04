import logging
import re
import json

from .message_handler import MessageHandler
from ..prompts.character import CharacterPrompts
from ..models.character import Character
from ..controllers.character import Character as controller
from discord import Embed


class CharacterHandler(MessageHandler):
    def __init__(self, discord_client, redis_client):
        super().__init__(discord_client, redis_client)
        self.controller = controller(discord_client, redis_client)
        self.command_handlers = {
            'create': self.create,
            'creation': self.creation,
            # 'add': self.add,
        }
        self.prompt_paths = {
            'creation': CharacterPrompts.character_create_path
        }

    def create(self, message, args, body=None):
        create_response = self.controller.create(message, args, body)
        return self.response(message, **create_response)

    def creation(self, message, args, body=None, prompt_state=None):
        creation_response = {}
        prompt_path = self.prompt_paths.get('creation')
        if prompt_state:
            # update character
            prompt_next_step = int(prompt_state['current_step']) + 1
            if len(prompt_path.keys()) > prompt_next_step:
                creation_response = { 'content': prompt_path[prompt_next_step]}
        else:
            stored_prompt_paths = self.redis_client.get('prompt_paths')
            if stored_prompt_paths:
                stored_prompt_paths = json.loads(stored_prompt_paths)
            else:
                stored_prompt_paths = {}

            stored_prompt_paths[message.author.id] = {
                'name': 'creation',
                'handler': 'character',
                'current_step': 0
            }
            self.redis_client.set('prompt_paths', json.dumps(stored_prompt_paths))
            creation_response = { 'content': prompt_path[0]['prompt'] }

        # creation_response = self.controller.creation(message, args, body)
        return self.response(message, **creation_response)

    def update(self, message, *args):
        return self.response(message, content="Let's make you a character")

    def delete(self, message, *args):
        return self.response(message, content="Let's make you a character")
