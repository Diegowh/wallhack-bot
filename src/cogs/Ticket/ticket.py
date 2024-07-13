import discord
from discord import app_commands
from discord.ext import commands
from src.views.create_ticket import CreateTicket
from src.utils import CommandName


class Ticket(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name=CommandName.TICKET)
    async def ticket(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            embed=discord.Embed(
                description="Press the button to create a new ticket!"
            ),
            view=CreateTicket()
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))


