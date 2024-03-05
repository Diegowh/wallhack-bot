import os

from dotenv import load_dotenv
import discord
from discord.ext import commands

from bot_state import BotState
from Cogs.server_scanner import ServerScanner
from Cogs.auto_interactions import AutoInteractions
import settings as settings
from utils import BotTokenName

load_dotenv() # Load .env file.
BOT_TOKEN = os.getenv(BotTokenName.DEVELOPMENT)

intents = discord.Intents.all() # need to enable
bot = commands.Bot(command_prefix='/', intents=intents)

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py') and not filename in ["__init__.py", "utils.py", "error.py"]:
        bot.load_extension(f'Cogs.{filename[:-3]}')


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
