import discord
from .bot import Bot

discord_client = discord.Client()
bot = Bot(discord_client)
command_prefix = '!'

@discord_client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(discord_client))

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    dm = False
    if isinstance(message.channel, discord.DMChannel) or message.content.startswith(command_prefix):
        if message.content.startswith(command_prefix):
            command_and_args = message.content.replace(command_prefix, '').split("\n")[0].split(" ")
            body = "\n".join(message.content.replace(command_prefix, '').split("\n")[1:])
        else:
            command_and_args = message.content.split("\n")[0].split(" ")
            body = "\n".join(message.content.split("\n")[1:])
            dm = True

        # Messages contain 3 parts, a command, arguments, and a body. Split on newlines to get command/args
        response_message = bot.dispatch_message(message, command_and_args, body, dm=dm)
        await response_message()


