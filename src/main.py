import os

from dotenv import load_dotenv
import discord
from discord.ext import commands

from bot_state import BotState
from cogs.server_scanner import ServerScanner
import settings as settings

load_dotenv()
# TODO: Change the way to select between dev and production tokens
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
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")

        bot_state.sync()
        print(f'We have logged in as {bot.user}')
        for command in bot.commands:
            print(f"Command {command.name} loaded.")

    except Exception as e:
        print(e)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to provide a map number.")
    else:
        raise error

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
