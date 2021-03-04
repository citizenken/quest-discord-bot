import os
import mongoengine
from discord.ext.commands import Bot
from . import settings
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
mongoengine.connect('quest-rpg-bot', host='localhost:27017')

d_bot = Bot(command_prefix=settings.COMMAND_PREFIX)

class QuestBot:
    def __init__(self):
        self.bot = d_bot
        self.redis = r

    def run(self):
        self.bot.run(settings.BOT_TOKEN)

quest_bot = QuestBot()

@quest_bot.bot.event
async def on_ready():
    print(f"I am {quest_bot.bot.user.name}")

    for file in os.listdir("./src/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            name = file[:-3]
            quest_bot.bot.load_extension(f"src.cogs.{name}")