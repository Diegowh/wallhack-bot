from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Optional

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import CommandName

if TYPE_CHECKING:
    from src.core.bot import Bot


class ServerScanner(commands.Cog):
    """Cog responsible for scanning ARK: Survival Ascended servers"""
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.settings = self.bot.settings.get("values")
        self.ark_data_manager = self.bot.ark_data_manager

        self.server_was_down: bool = False
        self.status_map_number: Optional[str] = None
        self.status_interaction: discord.Interaction | None = None

        self.lock = asyncio.Lock()
        self.active_status_tasks = {}

    @app_commands.command(
        name=CommandName.POP,
        description="Get the current pop of the specified ARK server"
    )
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

    @app_commands.command(
        name=CommandName.STATUS,
        description="Check the specified ARK server's status and notify when it is back online."
    )
    async def status(self, interaction: discord.Interaction, map_number: str):

        async with self.lock:
            if self.is_status_command_running(map_number):
                await interaction.response.send_message(f"I am already looking for {map_number} status")
                return

            self.active_status_tasks[map_number] = asyncio.create_task(self.status_task(interaction, map_number))

        await interaction.response.send_message(f"Started checking status for server {map_number}...")

    def is_status_command_running(self, map_number: str) -> bool:
        return map_number in self.active_status_tasks and not self.active_status_tasks[map_number].done()

    async def status_task(self, interaction: discord.Interaction, map_number: str, max_loops: int = 60):
        counter = 0
        server_was_down = False

        while counter < max_loops:
            is_down = await self.ark_data_manager.is_server_down(map_number)
            if is_down:
                server_was_down = False
            elif not is_down and server_was_down:
                member_role_id = self.settings.get('role_id_to_tag')
                role: discord.Role = discord.utils.get(interaction.guild.roles, id=int(member_role_id))
                await interaction.channel.send(f"{role.mention if role is not None else '@here'} {map_number} is up!")
                break
            else:
                counter += 1
                await asyncio.sleep(5)

        if counter >= max_loops:
            await interaction.followup.send(f"The server {map_number} is still up, try again.")
        async with self.lock:
            self.active_status_tasks.pop(map_number, None)


async def setup(bot: commands.Bot):
    await bot.add_cog(ServerScanner(bot))
