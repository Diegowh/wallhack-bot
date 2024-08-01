from __future__ import annotations

import asyncio
import json
import os
import time
from logging import getLogger
from typing import Optional

import discord
import psutil
from colorama import Fore, Back, Style
from discord.errors import DiscordServerError
from discord.ext import commands, tasks

from src.core.ark_data_manager import ARKDataManager
from src.core.embed import Embed
from src.settings import default_settings
from src.views.close_ticket import CloseTicket
from src.views.create_ticket import CreateTicket
from src.views.delete_ticket import DeleteTicket

log = getLogger("Bot")

__all__ = (
    "Bot",
)

prefix = (
        Fore.GREEN +
        f"[{time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}]" +
        Back.RESET +
        Fore.WHITE +
        Style.BRIGHT
)


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="/",
            intents=discord.Intents.all(),
            chunk_guild_at_startup=False
        )
        self.pid_file = "src/config/bot_pid.txt"
        self.owner_id = 184321136920756224
        self.ark_data_manager = ARKDataManager()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.settings_file_dir = os.path.join(self.script_dir, "settings.json")
        self.activity = discord.Activity(
                type=discord.ActivityType.playing,
                name="ARK: Survival Ascended"
            )
        self.message_ids = {}
        self.autopop_channel: Optional[discord.TextChannel] = None
        self.settings: dict | None = None

        self.maps_to_check: list[str] = ["2154", "2421"]
        self.id = 1205488021164662844

    async def on_ready(self) -> None:
        log.info(f"logged in as {Fore.YELLOW}{self.user}{Style.RESET_ALL}")
        await self.shutdown_previous_instance()
        self.settings = self.load_or_create_settings()
        await self.load_extensions()

        synced = await self.tree.sync()
        log.info(f"Slash CMDs Synced {Fore.YELLOW}{str(len(synced))} Commands{Style.RESET_ALL}")

        self.add_view(CreateTicket())
        self.add_view(CloseTicket())
        self.add_view(DeleteTicket())
        log.info(f"Views added {Fore.YELLOW}{len(self.persistent_views)} Views{Style.RESET_ALL}")

        self.autopop_channel = self.get_channel(1258888031285542992)  # ADAT disc channel
        if self.autopop_channel is None:
            self.autopop_channel = self.get_channel(1266307922611408972)  # DEV disc channel

        # Delete servers pop channel old msg
        await self.autopop_channel.purge(limit=4)
        self.start_auto_pop.start()

    async def shutdown_previous_instance(self):
        try:
            with open(self.pid_file, "r") as f:
                old_pid = int(f.read())

            process = psutil.Process(old_pid)
            process.terminate()
            process.wait()
            print(f"Previous bot instance with PID {old_pid} terminated")

        except psutil.NoSuchProcess:
            print("Previous bot instance not found")

        except psutil.AccessDenied:
            print("Access denied to terminate previous bot instance")

        except Exception as e:
            print(f"Failed to terminate previous bot instance: {e}")

    async def success(
            self,
            message: str,
            interaction: discord.Interaction,
            *,
            ephemeral: bool = False,
            embed: Optional[bool] = True
    ) -> Optional[discord.WebhookMessage]:

        if embed:
            if interaction.response.is_done():
                return await interaction.response.followup.send(
                    embed=Embed(description=message, color=discord.Color.green()),
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                embed=Embed(description=message,color=discord.Color.green()),
                ephemeral=ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(content=f"{message}", ephemeral=ephemeral)
            return await interaction.response.send_message(content=f"{message}", ephemeral=ephemeral)

    async def error(
            self,
            message: str,
            interaction: discord.Interaction,
            *,
            ephemeral: bool = False,
            embed: Optional[bool] = True
    ) -> Optional[discord.WebhookMessage]:

        if embed:
            if interaction.response.is_done():
                return await interaction.response.followup.send(
                    embed=Embed(description=message, color=discord.Color.red()),
                    ephemeral=ephemeral
                )
            return await interaction.response.send_message(
                embed=Embed(description=message,color=discord.Color.red()),
                ephemeral=ephemeral
            )
        else:
            if interaction.response.is_done():
                return await interaction.followup.send(content=f"{message}", ephemeral=ephemeral)
            return await interaction.response.send_message(content=f"{message}", ephemeral=ephemeral)

    @tasks.loop(seconds=45)
    async def start_auto_pop(self):

        try:
            if self.autopop_channel is None:
                log.error("Failed to get servers_pop_channel. Cancelling autopop task.")
                self.start_auto_pop.cancel()
                return

            for map_number in self.maps_to_check:
                embed = await self.ark_data_manager.get_embed(map_number)
                await self.send_or_edit_message(map_number, embed)

        except DiscordServerError as e:
            log.error(f"DiscordServerError in start_auto_pop: {e}, retrying loop in 180 seconds...")
            await asyncio.sleep(180)

        except Exception as e:
            log.exception(f"Unexpected error in start_auto_pop: {e}, retrying loop in 180 seconds...")
            await asyncio.sleep(180)

    async def send_or_edit_message(self, map_number, embed):
        if map_number in self.message_ids:
            message = await self.autopop_channel.fetch_message(self.message_ids[map_number])
            await message.edit(embed=embed)

        else:
            message = await self.autopop_channel.send(embed=embed)
            self.message_ids[map_number] = message.id

    def load_or_create_settings(self) -> dict:
        if not os.path.exists(self.settings_file_dir):
            log.warning("Settings file not found, creating new one...")
            self.save_settings(default_settings)
        with open(self.settings_file_dir, "r") as file:
            log.info("Settings loaded")
            return json.load(file)

    def save_settings(self, settings: dict) -> None:
        with open(self.settings_file_dir, "w") as file:
            json.dump(settings, file, indent=4)
            log.info("Settings saved")

    async def load_extensions(self):
        for root, _, files in os.walk("src/cogs"):
            for file in files:
                if file.endswith(".py") and file not in ["__init__.py", "utils.py"]:

                    extension = os.path.join(root, file)
                    extension = extension.replace("/", ".").replace("\\", ".")
                    extension = extension[:-3]  # Elimina .py

                    try:
                        await self.load_extension(extension)
                        log.info(f"Loaded extension {Fore.YELLOW}{extension}{Style.RESET_ALL}")
                    except Exception as e:
                        log.error(f"Failed to load extension {Fore.YELLOW}{extension}{Style.RESET_ALL}")
                        log.error(e)
