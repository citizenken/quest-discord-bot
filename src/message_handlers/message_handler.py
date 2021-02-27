import logging

class MessageHandler:
    def __init__(self, discord_client, redis_client, **kwargs):
        self.discord_client = discord_client
        self.redis_client = redis_client
        self.command_handlers = {}
        self.prompt_paths = {}
        self.logger = logging.getLogger('bot')


        for k, v in kwargs.items():
            self[k] = v

    def incoming(self, message, command_and_args, body):
        command = command_and_args.pop(0)
        command_and_args = command_and_args[1:]
        if command not in self.command_handlers.keys():
            return self.response(message, content="{} is an invalid command".format(command))
        return self.command_handlers[command](message, command_and_args, body)

    def prompt_path(self, message, command_and_args, body, prompt_state):
        if prompt_state['name'] in self.prompt_paths:
            command_handler = prompt_state['handler']
            return self.command_handlers[command_handler](message, command_and_args, body, prompt_state)

    def response(self, message, to_user=True, **sendArgs):
        async def author_response():
            await message.author.send(**sendArgs)

        async def channel_response():
            await message.channel.send(**sendArgs)

        if to_user is True:
            return author_response
        else:
            return channel_response
