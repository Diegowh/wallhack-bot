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
    ):

        time = self.convert_to_seconds(hours, minutes)
        await interaction.response.send_message(f"Timer set for {hours} hours and {minutes} minutes.", ephemeral=True)
        await asyncio.sleep(time)
        await interaction.followup.send(f"{interaction.user.mention}, {message}", ephemeral=True)

    @app_commands.command(name='notify')
    async def notify(
            self,
            interaction: discord.Interaction,
            message: str,
            hours: int,
            minutes: int,
    ):
        time = self.convert_to_seconds(hours, minutes)

        notification_msg = await interaction.channel.send(
            f"Timer set for {hours} hours and {minutes} minutes.\nReason: {message}\nReact with ⏰ to get notified!"
        )
        await notification_msg.add_reaction('⏰')
        await asyncio.sleep(time)

        notification_msg = await interaction.channel.fetch_message(notification_msg.id)
        users_to_notify = []

        for reaction in notification_msg.reactions:
            if reaction.emoji == '⏰':
                async for user in reaction.users():
                    if user != self.bot.id:
                        users_to_notify.append(user.mention)

        if users_to_notify:
            await interaction.channel.send(f"{message} \n{' '.join(users_to_notify)}")

    @staticmethod
    def convert_to_seconds(hours: int = 0, minutes: int = 0, seconds: int = 0) -> int:
        return hours * 3600 + minutes * 60 + seconds


async def setup(bot: commands.Bot):
    await bot.add_cog(Timer(bot))
