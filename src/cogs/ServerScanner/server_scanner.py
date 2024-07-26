from __future__ import annotations
import asyncio

import discord
from discord import app_commands
from discord.ext import commands, tasks
from src.utils import CommandName

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.bot import Bot


class ServerScanner(commands.Cog):
    """Cog responsible for scanning ARK: Survival Ascended servers"""
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.settings = self.bot.settings.get("values")
        self.ark_data_manager = self.bot.ark_data_manager

        self.server_was_down: bool = False
        self.status_map_number: str | None = None
        self.status_interaction: discord.Interaction | None = None

        self.lock = asyncio.Lock()
        self.active_status_loops: dict[str, dict[str, int | bool]] = {}

    @app_commands.command(name=CommandName.POP)
    async def pop(self, interaction: discord.Interaction, map_number: str):

        await interaction.response.defer(ephemeral=False)
        try:
            pop_embed = await self.ark_data_manager.get_embed(map_number)

            await interaction.followup.send(embed=pop_embed)

        except asyncio.TimeoutError:
            await interaction.followup.send("The request timed out. Try again later.")
        except Exception as e:
            await interaction.followup.send("An error occurred")
            print(f"An error occurred while fetching pop data: {e}")

    @app_commands.command(name=CommandName.STATUS)
    async def status(self, interaction: discord.Interaction, map_number: str):

        async with self.lock:
            if self.is_status_command_running(map_number):
                await interaction.response.send_message(f"I am already looking for {map_number} status")
                return

            self.active_status_loops[map_number] = {
                "counter": 0,
                "server_was_down": False,
            }
        self.status_task.start(interaction=interaction, map_number=map_number)

        await interaction.response.send_message(f"Started checking status for server {map_number}...")

    @tasks.loop(seconds=10)
    async def status_task(self, interaction: discord.Interaction, map_number: str, max_loops: int = 30):
        """
        Checks the status of a server periodically and sends notifications.

        Args:
            interaction (discord.Interaction): The interaction object.
            map_number (str): The map number to check the status for.
            max_loops (int, optional): The maximum number of times to check the status. Defaults to 40.
        """
        is_down = await self.ark_data_manager.is_server_down(map_number)
        async with self.lock:
            self.active_status_loops[map_number]["counter"] += 1
            server_was_down = self.active_status_loops[map_number].get("server_was_down", False)

            if is_down:
                self.active_status_loops[map_number]["server_was_down"] = True

            elif server_was_down and not is_down:
                member_role_id = self.settings.get('role_id_to_tag')
                role: discord.Role = discord.utils.get(interaction.guild.roles, id=int(member_role_id))
                await interaction.followup.send(f"{role.mention} {map_number} is up!")
                self.active_status_loops.pop(map_number)
                self.status_task.cancel()
                return

            if self.active_status_loops[map_number]["counter"] >= max_loops:
                await interaction.followup.send(f"The server {map_number} is still up, try again.")
                self.active_status_loops.pop(map_number)
                self.status_task.cancel()
                return

    @status_task.before_loop
    async def wait_until_bot_is_ready(self):
        """
        Waits for the bot to be ready before starting the status check task.
        """
        await self.bot.wait_until_ready()

    def is_status_command_running(self, map_number: str) -> bool:
        """
        Checks if a status check is currently running for a specific map number.

        Args:
            map_number (str): The map number to check.

        Returns:
            bool: True if a status check is running for the given map number, False otherwise.
        """
        return map_number in self.active_status_loops


async def setup(bot: commands.Bot):
    await bot.add_cog(ServerScanner(bot))
