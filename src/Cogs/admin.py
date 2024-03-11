from discord.ext import commands
import discord
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
            await self._show_settings(ctx)
            return

    async def _show_settings(self, ctx: commands.Context):

        embed = discord.Embed(title="Settings", color=discord.Color.blue())
        embed.add_field(name="Status command refresh interval", value=self.settings.status_sleep_interval, inline=False)
        embed.add_field(name="Status command timeout", value=self.settings.status_timeout, inline=False)
        embed.add_field(name="Autopop refresh interval", value=self.settings.autopop_sleep_interval, inline=False)
        embed.add_field(name="Autopop main map", value=self.settings.autopop_main_map, inline=False)
        embed.add_field(name="Role id to tag", value=self.settings.role_id_to_tag, inline=False)
        embed.add_field(name="Admin role id", value=self.settings.admin_role_id, inline=False)
        embed.add_field(name="Autopop channel id", value=self.settings.autopop_channel_id, inline=False)
        embed.add_field(name="Message id to preserve", value=self.settings.autopop_to_preserve_msg_id, inline=False)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
