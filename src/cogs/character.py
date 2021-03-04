import yaml
from discord.ext import commands

from ..models.character import Character as CharacterModel
from ..models.user import User
from ..prompts.character import CharacterPrompts
from ._base_cog import _BaseCog
from ..bot import quest_bot

class Character(_BaseCog):
    def __init__(self, quest_bot):
        super().__init__(quest_bot)

    @commands.group(pass_context=True,
                     invoke_without_command=True,
                     aliases=["me", "hp", "ap"])
    async def character(self, ctx, *arg):
        if ctx.invoked_with:
            if ctx.invoked_with == "me":
                await self.describe(ctx, *arg)
                return
            if ctx.invoked_with == "hp":
                await self.update_hp(ctx, int(arg[0]))
                return
            if ctx.invoked_with == "ap":
                await self.update_ap(ctx, int(arg[0]))
                return
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid git command passed...')

    @character.group(name='create',
                      description="Create a character",
                      brief="Create a character",
                      pass_context=True,
                      invoke_without_command=True)
    async def create(self, ctx):
        template = self.yaml_env.from_string(CharacterPrompts.character_create_prompt)
        response_text = template.render(creation_attrs=CharacterModel.creation_attrs)
        await self.response(ctx, **{ 'content': response_text })

    @create.command(name='submit',
                      description="Create a character",
                      brief="Create a character",
                      pass_context=True,
                      invoke_without_command=True)
    async def submit(self, ctx, *, form: str):
        yaml_lines = form.replace("```", "")

        for attr_name, prompt in CharacterModel.creation_attrs.items():
            yaml_lines = yaml_lines.replace(prompt, attr_name)

        attributes = yaml.safe_load(yaml_lines)
        character = CharacterModel(**attributes)
        character.create(self.quest_bot, ctx)

        embed = character.create_character_embed()
        await self.response(ctx, **{ 'embed': embed })

    @character.group(name='describe',
                      description="Describe a character",
                      brief="Describe a character",
                      pass_context=True,
                      invoke_without_command=True)
    async def describe(self, ctx, *arg):
        response_details = {}
        if not arg:
            embed = User.get_current_character(quest_bot, self.get_author_info(ctx)).create_character_embed()
            response_details = { 'content': "You are", 'embed': embed }
        else:
            character_name = arg[0]
            owner_info = arg[1].split("#")
            embed = CharacterModel.describe(character_name, owner_info[0], owner_info[1])

            if embed:
                response_details = { 'embed': embed }
            else:
                response_details = {
                    'content': 'No character named {name} owned by {owner_info} found. Was your input correct?'\
                        .format(name=character_name, owner_info="#".join(owner_info))
                }

        await self.response(ctx, **response_details)

    @character.group(name='list',
                      description="List the current users's character",
                      brief="List the current users's character",
                      pass_context=True,
                      invoke_without_command=True)
    async def list(self, ctx):
        list_of_characters = User.list_characters(quest_bot, self.get_author_info(ctx))
        template = self.yaml_env.from_string(CharacterPrompts.character_list_prompt)
        response_text = template.render(list_of_characters=list_of_characters)
        await self.response(ctx, **{ 'content': response_text })

    @character.group(name='update',
                      description="Update a character",
                      brief="Update a character",
                      pass_context=True,
                      invoke_without_command=True)
    async def update(self, ctx, *arg):
        pass

    @update.command(name='hp',
                      description="Update a character",
                      brief="Update a character",
                      pass_context=True,
                      invoke_without_command=True)
    async def update_hp(self, ctx, change: int):
        character = User.get_current_character(quest_bot, self.get_author_info(ctx))
        character.hp = character.update_hp(change)
        await self.response(ctx, **{ 'content': '{name} now has {hp} hit points'.format(name=character.name, hp=character.hp) })

    @update.command(name='ap',
                      description="Update a character",
                      brief="Update a character",
                      pass_context=True,
                      invoke_without_command=True)
    async def update_ap(self, ctx, change: int):
        character = User.get_current_character(quest_bot, self.get_author_info(ctx))
        character.update_ap(change)
        await self.response(ctx, **{ 'content': '{name} now has {ap} ability points'.format(name=character.name, ap=character.ap) })

def setup(d_bot):
    d_bot.add_cog(Character(quest_bot))