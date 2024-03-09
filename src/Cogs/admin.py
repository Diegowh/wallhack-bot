from discord.ext import commands
import discord
from src import settings
from src.utils import CommandName


class Admin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.settings = self.bot.settings

    def is_admin(self, ctx: commands.Context):
        author_role_ids = [role.id for role in ctx.author.roles]
        return ctx.author.guild_permissions.administrator or self.settings.admin_role_id in author_role_ids

    @commands.command(name=CommandName.SETTINGS)
    async def settings(self, ctx: commands.Context, *args):

        if not self.is_admin(ctx):
            return

        if not args:
            # Show actual settings
            ...
