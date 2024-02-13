import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from server_data import ServerData

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
server_data = ServerData()


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command/s")
    except Exception as e:
        print(e)


@bot.tree.command(name="pop")
async def pop(interaction: discord.Interaction, server_number: int = 2154):
    pop_msg = server_data.pop()

    embed = discord.Embed(title=f"TheIsland{server_number}", color=0x00ff00)
    embed.add_field(name="Active Players", value=pop_msg, inline=True)
    await interaction.response.send_message(embed=embed)


bot.run(TOKEN)
