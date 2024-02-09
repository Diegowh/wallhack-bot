import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def pop(ctx):
    pop_msg = "Command /pop was called"
    await ctx.send(pop_msg)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Relax bro, try again in {:d}s. UwU'.format(
            round(error.retry_after))
        await ctx.send(msg)
    else:
        raise error

TOKEN = os.getenv("BOT_TOKEN")
bot.run(TOKEN)
