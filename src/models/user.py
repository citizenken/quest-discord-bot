from mongoengine import *
from bson import ObjectId
import json
import redis
from .. import settings

r = redis.Redis(settings.REDIS_CONFIG)

class User(Document):
    discord_id = LongField(required=True)
    name = StringField(required=True)
    discriminator = StringField(required=True)
    characters = ListField(ReferenceField('Character'), default=[])
    current_character = ReferenceField('Character', default=None)

    def get_user_from_session(quest_bot, author):
        user = None
        session = quest_bot.redis.get(author['id'])
        if not session:
            users = User.objects(discord_id=author['id'])
            if not users:
                user = User(discord_id=author['id'], name=author['name'], discriminator=author['discriminator'])
            else:
                user = users[0]
            user.save()
            user.update_user_session(quest_bot, author['id'])
        else:
            session = json.loads(session)
            user = User(**session)
        return user

    def update_user_session(self, quest_bot, author_id):
        raw_user_dict = self.to_mongo().to_dict()
        user_dict = {}
        for key, value in raw_user_dict.items():
            to_write = raw_user_dict[key]
            if isinstance(to_write, ObjectId) or (isinstance(to_write, list) and any(isinstance(i, ObjectId) for i in to_write)):
                if isinstance(to_write, list):
                    to_write = [str(i) for i in to_write]
                else:
                    to_write = str(to_write)

            if key.startswith('_'):
                user_dict[key.replace('_','')] = to_write
            else:
                user_dict[key] = to_write

        quest_bot.redis.setex(author_id, 500, json.dumps(user_dict))

    def get_current_character(quest_bot, author):
        user = User.get_user_from_session(quest_bot, author)
        return user.current_character

    def describe_owned_character(quest_bot, author, character_name):
        user = User.get_user_from_session(quest_bot, author)
        character = [character for c in user.characters if c.name is character_name]
        return character.create_character_embed()

    def list_characters(quest_bot, author):
        user = User.get_user_from_session(quest_bot, author)
        return user.characters

