from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import CommandName

if TYPE_CHECKING:
    from src.core.bot import Bot


class Timer(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(name=CommandName.TIMER)
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

    @app_commands.command(name=CommandName.NOTIFY)
    async def notify(
            self,
            interaction: discord.Interaction,
            message: str,
            hours: int,
            minutes: int,
    ):
        await interaction.response.defer(ephemeral=False)

        sleep_time = self.convert_to_seconds(hours, minutes)
        unix_time = int(time.time()) + sleep_time

        notification_msg = await interaction.followup.send(
            f"**{message}** <t:{unix_time}:R>\nReact with ⏰ to get notified!"
        )

        notification_msg = await interaction.channel.fetch_message(notification_msg.id)
        await notification_msg.add_reaction('⏰')
        await asyncio.sleep(sleep_time)

        notification_msg = await interaction.channel.fetch_message(notification_msg.id)
        users_to_notify = []

        for reaction in notification_msg.reactions:
            if reaction.emoji == '⏰':
                async for user in reaction.users():
                    if user.id != self.bot.user.id:
                        users_to_notify.append(user.mention)

        if users_to_notify:
            # Elimino las posibles menciones hechas en el mensaje de notificacion,
            # para evitar mencionar a personas que no hayan reaccionado al mensaje
            message = self.remove_role_mentions(message)
            await interaction.channel.send(f"**{message}** \n{' '.join(users_to_notify)}")

    @staticmethod
    def convert_to_seconds(hours: int = 0, minutes: int = 0, seconds: int = 0) -> int:
        return hours * 3600 + minutes * 60 + seconds

    @staticmethod
    def remove_role_mentions(message: str) -> str:
        words = message.split()
        filtered_words = [word for word in words if not word.startswith('<@')]
        return ' '.join(filtered_words)


async def setup(bot: commands.Bot):
    await bot.add_cog(Timer(bot))
