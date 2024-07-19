import discord
from discord import app_commands
from discord.ext import commands
from src.views.create_ticket import CreateTicket
from src.utils import CommandName


class Ticket(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name=CommandName.TICKET, description="Opens a ticket")
    async def ticket(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=discord.Embed(
                description="Press the button to create a new ticket!"
            ),
            view=CreateTicket()
        )

    @app_commands.command(name=CommandName.ADD, description="Adds a user to the ticket")
    async def add(self, interaction: discord.Interaction, user: discord.Member):
        channel = interaction.channel

        if isinstance(channel, discord.TextChannel):

            await channel.set_permissions(user, send_messages=True, read_messages=True)
            await interaction.response.send_message(
                f"{user.mention} has been added to the ticket."
            )

    @app_commands.command(name=CommandName.REMOVE, description="Removes a user from the ticket")
    async def remove(self, interaction: discord.Interaction, user: discord.Member):
        channel = interaction.channel

        if isinstance(channel, discord.TextChannel):

            await channel.set_permissions(user, send_messages=False, read_messages=False)
            await interaction.response.send_message(
                f"{user} has been removed from the ticket."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))


