from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from src.core.bot import Bot
from src.utils import CommandName
from src.views.create_ticket import CreateTicket


class Ticket(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name=CommandName.TICKET,
        description="Opens a ticket. Press the button to create a ticket"
    )
    async def ticket(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=discord.Embed(
                description="Press the button to create a new ticket!"
            ),
            view=CreateTicket()
        )

    @app_commands.command(
        name=CommandName.ADD,
        description="Adds a user to the current ticket, allowing them to view and send messages."
    )
    async def add(self, interaction: discord.Interaction, user: discord.Member):
        channel = interaction.channel

        if isinstance(channel, discord.TextChannel):

            await channel.set_permissions(user, send_messages=True, read_messages=True)
            await interaction.response.send_message(
                f"{user.mention} has been added to the ticket."
            )

    @app_commands.command(
        name=CommandName.REMOVE,
        description="Removes a user from the current ticket, revoking their view and send permissions."
    )
    async def remove(self, interaction: discord.Interaction, user: discord.Member):
        channel = interaction.channel

        if isinstance(channel, discord.TextChannel):

            await channel.set_permissions(user, send_messages=False, read_messages=False)
            await interaction.response.send_message(
                f"{user} has been removed from the ticket."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))


