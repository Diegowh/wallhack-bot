from __future__ import annotations

import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.bot import Bot


class Timer(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(name='timer')
    async def timer(
            self,
            interaction: discord.Interaction,
            message: str,
            hours: int,
            minutes: int,
            seconds: int
    ):

        time = self.convert_to_seconds(hours, minutes, seconds)

        await interaction.response.send_message(f"Timer set for {hours:02}:{minutes:02}:{seconds:02} ", ephemeral=True)
        await asyncio.sleep(time)
        await interaction.followup.send(message, ephemeral=True)

    @staticmethod
    def convert_to_seconds(hours: int, minutes: int, seconds: int) -> int:
        return hours * 3600 + minutes * 60 + seconds


async def setup(bot: commands.Bot):
    await bot.add_cog(Timer(bot))
