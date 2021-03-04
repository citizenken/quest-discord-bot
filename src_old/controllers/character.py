import logging
import re

from .controller import Controller
from ..models.character import Character as CharacterModel
from discord import Embed
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('src', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

class Character(Controller):
    def __init__(self, discord_client, redis_client):
        super().__init__(discord_client, redis_client)

    def create(self, message, args, body=None):
        if not body:
            return self.show_create_prompt(message, args)
        else:
            return self.parse_create_prompt(message, body)

    def show_create_prompt(self, message, args):
        template = env.get_template('character_create_prompt.j2')
        response_text = template.render(character_prompts=CharacterModel.prompt_texts())
        return { 'content': response_text }

    def parse_create_prompt(self, message, body):
        regex = CharacterModel.prompt_regexes()
        matches = re.search(regex, body)
        if not hasattr(matches, 'groupdict'):
            return { 'content': 'It looks like the form wasn\'t filled out quite right. Please try again' }
        match_groups = matches.groupdict()

        for k in list(match_groups.keys()):
            if re.search("\d+", k):
                singular_key = re.sub("\d+", "", k)
                plural_key = "{}s".format(singular_key)
                if not match_groups.get(plural_key):
                    match_groups[plural_key] = []
                value = match_groups.pop(k, None)
                match_groups[plural_key].append(value)

        character = CharacterModel(message, **match_groups)

        character.description = body.replace('`', '').strip()
        embed = self.create_character_embed(message, character)
        return { 'embed': embed }

    def create_character_embed(self, message, character):
        embed_details = {
            'title': character.name,
            'description': character.description,
        }
        embed = Embed(**embed_details)\
            .set_author(name=character.owner_name)\
            .add_field(name='\u200B', value='\u200B', inline=False)\
            .add_field(name='HP', value=character.hp)\
            .add_field(name='AP',value=character.ap)
        if len(character.inventory) > 0:
            embed.add_field(name='Inventory', value=", ".join(character.inventory), inline=False)
        else:
            embed.add_field(name='Inventory', value="Empty", inline=False)

        if character.image:
            embed.set_image(url=character.image)

        return embed

    # def add