from discord.ext import commands
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('src', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

class _BaseCog(commands.Cog):
    def __init__(self, quest_bot):
        self.quest_bot = quest_bot
        self.yaml_env = env

    def parse_yaml(argument):
        return argument.upper()

    def get_author_info(self, ctx):
        return {
            'id': ctx.author.id,
            'name': ctx.author.name,
            'discriminator': ctx.author.discriminator,
        }

    def parse_message(self, ctx):
        content = ctx.message.content
        command_and_args = ctx.content.split("\n")[0].split(" ")
        body = "\n".join(ctx.content.split("\n")[1:])
        return command_and_args, body

    async def response(self, ctx, to_user=True, **send_args):
        if to_user is True:
            await ctx.author.send(**send_args)
        else:
            await ctx.channel.send(**send_args)