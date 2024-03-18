import discord
from discord import Embed, app_commands
from discord.ext import commands
from utils import time_to_unix


class BreederHelper(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.settings = self.bot.settings

    @app_commands.command(name="claims",description=f"Makes a ping in that the member know u giving out tames")
    async def claims(
            #Args of the SlashCommand
            self,
            interaction: discord.Interaction,
            tame: str,
            when: int,
            where: str
    ) -> None:
        if interaction.user.get_role(self.settingsrole_breeder_id):
            embed = Embed(title=f'Claims for:  {tame}', description=f"{self.settings.role_to_tag} Please react if u need!")
            embed.add_field(name="When: ", value=f'<t:{int(time_to_unix(when))}:R>', inline=True)
            embed.add_field(name=" ", value=" ", inline=False)
            embed.add_field(name="Where:", value=f'{where}', inline=True)
            await interaction.response.send_message(embed=embed)
        else:
            embed = Embed(title="Access denied", description="You dont have the Breeder Role :(")
            await interaction.response.send_message(embed= embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(BreederHelper(bot))