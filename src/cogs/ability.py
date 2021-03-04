from discord.ext import commands
import yaml
import operator
import functools

from ..prompts.character import CharacterPrompts
from ._base_cog import _BaseCog
from ..bot import quest_bot
from ..models.ability import Ability as AbilityModel

class Ability(_BaseCog):
    def __init__(self, quest_bot):
        super().__init__(quest_bot)

    @commands.group(pass_context=True,
                     invoke_without_command=True)
    async def ability(self, ctx, *, arg):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid git command passed...')

    @ability.group(name='create',
                      description="Create an ability",
                      brief="Create an ability",
                      pass_context=True,
                      invoke_without_command=True)
    async def create(self, ctx):
        # template = env.from_string(CharacterPrompts.character_create_prompt)
        # response_text = template.render(creation_attrs=CharacterModel.creation_attrs)
        # await self.response(ctx, **{ 'content': response_text })
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid ability create command passed...')

    @create.command(name='submit',
                      description="Create a character",
                      brief="Create a character",
                      pass_context=True,
                      invoke_without_command=True)
    async def submit(self, ctx, *, form=None):
        if form:
            yaml_lines = form.replace("```", "")
        elif ctx.message.attachments:
            yaml_lines = await ctx.message.attachments[0].read()

        loaded = yaml.safe_load(yaml_lines)

        response_details = {}
        if isinstance(loaded, list):
            created = []
            for ability_attrs in loaded:
                ability = AbilityModel(**ability_attrs)
                ability.create(**ability_attrs)
                created.append(ability)
            response_details = { 'content': '\n'.join([c.name for c in created]) }
        else:
            ability = AbilityModel(**loaded)
            ability.create(**loaded)
            created.append(ability)
            response_details = { 'content': ability.name }

        await self.response(ctx, **response_details)

def setup(d_bot):
    d_bot.add_cog(Ability(quest_bot))