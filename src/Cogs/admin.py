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
        embed = self._create_settings_embed()
        await ctx.send(embed=embed)

    def _create_settings_embed(self):
        embed = discord.Embed(title="Settings", color=discord.Color.blue())
        for command_data in self.settings.data.values():
            embed.add_field(
                name=f"{command_data['id']} - {command_data['name']}",
                value=command_data["value"],
                inline=False
            )
        return embed


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
