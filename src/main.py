import os

from dotenv import load_dotenv
import json
import discord
from discord.ext import commands
from bot_state import BotState
from utils import BotTokenName
from settings import default_settings


load_dotenv() # Load .env file.
BOT_TOKEN = os.getenv(BotTokenName.DEVELOPMENT)


intents = discord.Intents.all()  # need to enable
bot = commands.Bot(command_prefix='/', intents=intents)

script_dir = os.path.dirname(os.path.abspath(__file__))
settings_file_dir = os.path.join(script_dir, "settings.json")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    bot.settings = load_or_create_settings()
    await load_extensions()
    bot.state = BotState(bot)
    bot.state.sync()


def load_or_create_settings() -> dict:
    print("Trying to load settings...")
    if not os.path.exists(settings_file_dir):
        print("Settings file not found, creating new one...")
        save_settings(default_settings)
    with open(settings_file_dir, "r") as file:
        print("Settings loaded")
        return json.load(file)
    
def save_settings(settings: dict) -> None:
    with open(settings_file_dir, "w") as file:
        json.dump(settings, file, indent=4)
        print("Settings saved")
        
        
async def load_extensions():
    for filename in os.listdir("src/Cogs"):
        if filename == "__pycache__":
            pass
        elif filename.endswith('.py') and filename not in ["__init__.py", "utils.py", "error.py"]:
            try:
                await bot.load_extension(f'Cogs.{filename[:-3]}')
                print(f'Loaded extension {filename[:-3]}')
            except Exception as e:
                print(f'Failed to load extension {filename[:-3]}')
                print(e)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
