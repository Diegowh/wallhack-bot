import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from server_pop import ServerData

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
SERVER_ID = os.getenv("SERVER_ID")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
server_data = ServerData(server_id=SERVER_ID)

# When the Bot starts


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command/s")
    except Exception as e:
        print(e)


# Pop command
@bot.tree.command(name="pop", description="Gives the server pop of 2154")
async def pop(interaction: discord.Interaction):
    msg = server_data.pop()
    await interaction.response.send_message(msg)


# @bot.tree.command(name="test", description="test command")
# async def test(interaction: discord.Interaction):
#     pop_msg = server_data.pop()

#     embed = discord.Embed(title="TheIsland2154", color=0x00ff00)
#     embed.add_field(name="Population", value=pop_msg, inline=True)
#     await interaction.response.send_message(embed=embed)

# Synronize the bot with the server commands. I only use it the very first time I start the bot. Unsure if it's necessary at all.


bot.run(TOKEN)
