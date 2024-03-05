import os

from dotenv import load_dotenv
import discord
from discord.ext import commands
from bot_state import BotState
import asyncio
import settings as settings
from utils import BotTokenName

load_dotenv() # Load .env file.
BOT_TOKEN = os.getenv(BotTokenName.PRODUCTION)

intents = discord.Intents.all() # need to enable
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await load_extensions()
    bot.state = BotState(bot)
    bot.state.sync()

async def load_extensions():
    for filename in os.listdir("src/Cogs"):
        if filename == "__pycache__": pass
        elif filename.endswith('.py') and not filename in ["__init__.py", "utils.py", "error.py"]:
            try:
                await bot.load_extension(f'Cogs.{filename[:-3]}')
            except Exception as e:
                print(f'Failed to load extension {filename[:-3]}')
                print(e)

if __name__ == "__main__":
    bot.run(BOT_TOKEN)