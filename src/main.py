import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from src.bot_state import BotState
from src.cogs.server_scanner import ServerScanner

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Discord intents setup
intents = discord.Intents.default()
intents.message_content = True

# Bot instance
bot = commands.Bot(command_prefix='/', intents=intents)
bot_state = BotState(bot=bot)


@bot.event
async def on_ready():
    """
    Its called when the bot is connected to Discord. Its used to sync the commands and for debugging purposes.
    """
    await bot.add_cog(ServerScanner(bot=bot, bot_state=bot_state))
    print(f'{bot.user} has connected to Discord!')
    try:
        bot_state.sync()
        print(f'We have logged in as {bot.user}')
        for command in bot.commands:
            print(f"Command {command.name} loaded.")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
