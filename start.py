from src.bot import quest_bot
import logging
import sys

bot_logger = logging.getLogger('bot')
bot_logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S')
ch.setFormatter(formatter)
bot_logger.addHandler(ch)

quest_bot.run()