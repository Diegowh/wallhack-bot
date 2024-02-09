import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from server_pop import ServerData

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
server_data = ServerData()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.tree.command(name="pop", description="Gives the server pop of 2154")
async def pop(interaction: discord.Interaction):
    msg = server_data.pop()
    await interaction.response.send_message(msg)


@bot.command()
async def syncronize(ctx):
    await bot.tree.sync()
    await ctx.send("Ready!")


bot.run(TOKEN)
