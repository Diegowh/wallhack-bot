import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.tree.command(name="pop", description="Gives the server pop")
async def pop(interaction: discord.Interaction):
    await interaction.response.send_message("Command /pop was called")


@bot.command()
async def syncronize(ctx):
    await bot.tree.sync()
    await ctx.send("Ready!")


bot.run(TOKEN)
