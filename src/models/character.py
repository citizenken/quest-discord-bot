import uuid
from ..prompts.character import CharacterPrompts

class Character:
    def __init__(self, message, name=None, pronouns=None, age=None, height=None, role=None,
    features=None, clothing=None, movement=None, home=None, culture=None, belief=None,
    flaw=None, dream=None, inventory=[],description=None, image=None, **kwargs):
        self.id = uuid.uuid4()
        self.owner_id = message.author.id
        self.owner_name = message.author.name
        self.hp = 10
        self.ap = 5
        self.name = name
        self.pronouns = pronouns
        self.age = age
        self.height = height
        self.role = role
        self.features = features
        self.clothing = clothing
        self.movement = movement
        self.home = home
        self.culture = culture
        self.belief = belief
        self.flaw = flaw
        self.dream = dream
        self.inventory = inventory
        self.description = description
        self.image = "https://www.adventure.game/static/fighter-cutout-7d9c48c2d1c848eef49b940448f986dc.png"

    @staticmethod
    def prompt_texts():
        return "\n".join([details['text'] for prompt_name, details in CharacterPrompts.character_template_prompts.items()])

    @staticmethod
    def prompt_regexes():
        return "\n".join([details['regex'] for prompt_name, details in CharacterPrompts.character_template_prompts.items()])

