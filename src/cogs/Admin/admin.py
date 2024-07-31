from __future__ import annotations

import os
import sys

import discord
from discord import app_commands
from discord.ext import commands

from src.core.bot import Bot
from src.utils import CommandName


class Admin(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.settings = self.bot.settings.get("values")

    @app_commands.command(name=CommandName.RESTART, description="Restarts the bot. Don't use it unless it is totally necessary.")
    async def restart(self, interaction: discord.Interaction):
        await interaction.response.send_message("Restarting bot...", ephemeral=True)

        with open(self.bot.pid_file, "w") as f:
            f.write(str(os.getpid()))

        await self.bot.close()
        if self.bot.is_closed():
            print(f"Bot is closed!")
            os.execv(sys.executable, ['python'] + sys.argv)


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
