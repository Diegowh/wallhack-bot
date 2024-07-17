import os
import sys

import discord
from discord.ext import commands
from discord import app_commands
from src.utils import CommandName


class Admin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.settings = self.bot.settings.get("values")

    @app_commands.command(name="restart", description="Restarts the bot.")
    async def restart(self, interaction: discord.Interaction):
        await interaction.response.send_message("Restarting bot...", ephemeral=True)
        os.execv(sys.executable, ['python'] + sys.argv)


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
