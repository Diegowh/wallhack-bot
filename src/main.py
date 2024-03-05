import os

from dotenv import load_dotenv
import discord
from discord.ext import commands

from bot_state import BotState
from cogs.server_scanner import ServerScanner
from cogs.auto_interactions import AutoInteractions
import settings as settings
from utils import BotTokenName

load_dotenv() # Load .env file.
BOT_TOKEN = os.getenv(BotTokenName.DEVELOPMENT)

# Discord intents setup
intents = discord.Intents.all()

# Bot instance
bot = commands.Bot(command_prefix='/', intents=intents)
bot_state = BotState(bot=bot)


@bot.event
async def on_ready():
    """
    Its called when the bot is connected to Discord. Its used to sync the commands and for debugging purposes.
    """
    await bot.add_cog(ServerScanner(bot=bot, bot_state=bot_state))
    await bot.add_cog(AutoInteractions(bot=bot))
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")

        bot_state.sync()
        print(f'We have logged in as {bot.user}')
        for command in bot.commands:
            print(f"Command {command.name} loaded.")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
