import asyncio
from asyncio import tasks
import os

from dotenv import load_dotenv
import json
import discord
from discord.ext import commands, tasks
from bot_state import BotState
from server_data import ServerData
from utils import BotTokenName
from config.config import (
    DEVELOPMENT_BOT_TOKEN,
    PRODUCTION_BOT_TOKEN,
)
from settings import default_settings


intents = discord.Intents.all()  # need to enable
bot = commands.Bot(command_prefix='/', intents=intents)

script_dir = os.path.dirname(os.path.abspath(__file__))
settings_file_dir = os.path.join(script_dir, "settings.json")

message_ids = {}


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

    bot.settings = load_or_create_settings()
    await load_extensions()
    bot.state = BotState(bot)
    bot.state.sync()
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} slash commands")

    # Delete servers pop channel old msg
    servers_pop_channel = bot.get_channel(1258888031285542992)
    if servers_pop_channel:
        # Delete previous msg
        await servers_pop_channel.purge(limit=4)

    start_auto_pop.start()


@tasks.loop(seconds=30)
async def start_auto_pop():
    server_data_manager = ServerData()

    maps_to_check = ["2154", "2421"]
    servers_pop_channel = bot.get_channel(1258888031285542992)

    for map_number in maps_to_check:

        map_data = await server_data_manager.fetch_map_data(map_number=map_number)
        await asyncio.sleep(1)

        if map_data is None:
            embed = server_data_manager.create_error_embed(
                title="Server not found",
                description="Server is down"
            )
            if map_number in message_ids:
                message = await servers_pop_channel.fetch_message(message_ids[map_number])
                await message.edit(embed=embed)

            else:
                message = await servers_pop_channel.send(embed=embed)
                message_ids[map_number] = message.id
        else:
            players = map_data["totalPlayers"]
            max_players = map_data["settings"]["maxPublicPlayers"]

            pop_embed = server_data_manager.create_pop_message(map_data=map_data)

            if map_number in message_ids:
                message = await servers_pop_channel.fetch_message(message_ids[map_number])
                await message.edit(embed=pop_embed)
            else:
                message = await servers_pop_channel.send(embed=pop_embed)
                message_ids[map_number] = message.id


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
    bot.run(PRODUCTION_BOT_TOKEN)
