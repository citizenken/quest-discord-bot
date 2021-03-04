import uuid
from mongoengine import *

from ..prompts.character import CharacterPrompts
from discord import Embed
from .user import User

class Character(Document):
    owner = ReferenceField('User')
    hp = IntField(required=True, default=10)
    ap = IntField(required=True, default=5)
    name = StringField(required=True)
    pronouns = StringField()
    age = IntField()
    height = StringField()
    role = StringField()
    features = StringField()
    clothing = StringField()
    movement = StringField()
    home = StringField()
    culture = StringField()
    belief = StringField()
    flaw = StringField()
    dream = StringField()
    inventory = ListField(default=[])
    image     = StringField()

    creation_attrs = {
        "name": "My name is",
        "pronouns": "My pronouns are",
        "age": "I'm this old",
        "height": "I'm this tall",
        "role": "My role in the party is",
        "features": "When people see me, they first notice my",
        "clothing": "I wear",
        "movement": "I move with",
        "home": "I'm from",
        "culture": "Where my people are known for",
        "belief": "I believe in",
        "flaw": "This side of me can get in the way",
        "dream": "I dream of"
        }

    list_attrs = ['inventory']

    # def __init__(self, ctx, name=None, pronouns=None, age=None, height=None, role=None,
    # features=None, clothing=None, movement=None, home=None, culture=None, belief=None,
    # flaw=None, dream=None, inventory=[], description=None, image=None, **kwargs):
    #     self.id = uuid.uuid4()
    #     self.owner_id = ctx.author.id
    #     self.owner_name = ctx.author.name
    #     self.hp = 10
    #     self.ap = 5
    #     self.name = name
    #     self.pronouns = pronouns
    #     self.age = age
    #     self.height = height
    #     self.role = role
    #     self.features = features
    #     self.clothing = clothing
    #     self.movement = movement
    #     self.home = home
    #     self.culture = culture
    #     self.belief = belief
    #     self.flaw = flaw
    #     self.dream = dream
    #     self.inventory = inventory
    #     self.image = "https://www.adventure.game/static/fighter-cutout-7d9c48c2d1c848eef49b940448f986dc.png"

    @staticmethod
    def prompt_texts():
        return "\n".join([details['text'] for prompt_name, details in CharacterPrompts.character_template_prompts.items()])

    @staticmethod
    def prompt_regexes():
        return "\n".join([details['regex'] for prompt_name, details in CharacterPrompts.character_template_prompts.items()])

    def build_description(self):
        self_as_dict = self.to_mongo().to_dict()
        for key in Character.creation_attrs.keys():
            if not self_as_dict.get(key, None):
                self_as_dict[key] = None

        description_template = """
My name is {name}, my pronouns are {pronouns}
I'm {age} years old and stand {height} tall.
I'm the party's {role}
When people see me, they first notice my {features}
I wear {clothing} and move with {movement}
I'm from {home} where my people are known for {culture}
I believe in {belief} but my {flaw} side can get in my way.
I dream of {dream}""".format(**self_as_dict)
        return description_template

    def create_character_embed(self):
        embed_details = {
            'title': self.name,
            'description': self.build_description(),
        }

        embed = Embed(**embed_details)\
            .set_author(name="{}#{}".format(self.owner.name, self.owner.discriminator))\
            .add_field(name='\u200B', value='\u200B', inline=False)\
            .add_field(name='HP', value=self.hp)\
            .add_field(name='AP',value=self.ap)
        if len(self.inventory) > 0:
            embed.add_field(name='Inventory', value=", ".join(self.inventory), inline=False)
        else:
            embed.add_field(name='Inventory', value="Empty", inline=False)

        if self.image:
            embed.set_image(url=self.image)

        return embed

    def create(self, quest_bot, ctx):
        if not self.owner:
            self.owner = User.get_user_from_session(quest_bot, ctx)
        self.save()

        # Update owner
        self.owner.characters.append(self)

        if not self.owner.current_character:
            self.owner.current_character = self
        self.owner.save()
        self.owner.update_user_session(quest_bot, ctx)

    def describe(name, owner_name, discriminator):
        characters = Character.objects(name=name)
        matching_character = None
        if characters:
            for character in characters:
                if character.owner and \
                    character.owner.name == owner_name and \
                        character.owner.discriminator == discriminator:
                    matching_character = character
                    # Just return the first match
                    break

        if matching_character:
            return matching_character.create_character_embed()
        else:
            return None

    def update_hp(self, change: int):
        self.hp = self.hp + change
        self.save()

    def update_ap(self, change: int):
        self.ap = self.ap + change
        self.save()
