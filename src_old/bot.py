import logging
import json

import mongoengine
from .message_handlers.message_handler import MessageHandler
from .message_handlers.character import CharacterHandler

import redis
r = redis.Redis(host='localhost', port=6379, db=0)
mongoengine.connect('project1')

class Bot:
    def __init__(self, discord_client):
        self.logger = logging.getLogger('bot')
        self.discord_client = discord_client
        self.redis_client = r
        self.default_handler = MessageHandler(self.discord_client, self.redis_client)
        self.handlers = {
            'character': CharacterHandler(self.discord_client, self.redis_client)
        }
        self.default_handler.command_handlers = self.handlers

    def dispatch_message(self, message, command_and_args, body, dm=False):
        prompt_paths = None
        dispatch_to = None
        command = command_and_args.pop(0)

        if dm:
            # Prompt paths are only allowed via dm
            prompt_paths = self.redis_client.get('prompt_paths')
            if prompt_paths is None:
                prompt_paths = {}
            else:
                prompt_paths = json.loads(prompt_paths)
            current_prompt = prompt_paths.get(str(message.author.id), None)
            if current_prompt:
                dispatch_to = self.handlers.get(current_prompt['handler'], None)
            else:
                dispatch_to = self.handlers.get(command, None)
        else:
            dispatch_to = self.handlers.get(command, None)

        import pdb; pdb.set_trace()
        # If command handler is found, and prompt is found, assume
        # starting a new command with `!command`. Clear current prompt status
        if dispatch_to and current_prompt and command in self.handlers:
            self.logger.debug('Handler found, prompt found')
            # Clear prompt path from redis since user has started new command
            prompt_paths.pop(str(message.author.id))
            self.redis_client.set('prompt_paths', json.dumps(prompt_paths))
            response = dispatch_to.incoming(message, command_and_args, body)
        # If no handler is found, assume they are responding on a prompt path. Continue
        elif dispatch_to and current_prompt and command not in self.handlers:
            response = dispatch_to.prompt_path(message, command_and_args, body, current_prompt)
        # If handler is found but not prompt path, handle the command
        elif dispatch_to and not current_prompt:
            response = dispatch_to.incoming(message, command_and_args, body)
        else:
            self.logger.debug('Handler not found, no prompt found')
            error_handler = self.default_handler
            response = error_handler.response(message, **{'content': 'Command {} is invalid'.format(command)})
            # response = dispatch_to.incoming(message, command_and_args, body)

        return response

    def start_discord_client(self):
        self.discord_client.run('ODE0MTc2NzY2NDg2MjQ5NDky.YDaDMw.PmoKAh2mBXWQltxlEd6k16JRHj8')

