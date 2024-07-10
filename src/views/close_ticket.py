from . import *
from .delete_ticket import DeleteTicket


class CloseTicket(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close the ticket", style=discord.ButtonStyle.red, custom_id="close_ticket", emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer(ephemeral=True)

        await interaction.channel.send("Closing this ticket in 3 seconds!")

        await asyncio.sleep(3)

        category: discord.CategoryChannel = discord.utils.get(
            interaction.guild.categories,
            id=CLOSED_TICKETS_CATEGORY_ID
        )
        role: discord.Role = interaction.guild.get_role(MEMBER_ROLE_ID)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await interaction.channel.edit(category=category)
        await interaction.channel.send(
            embed=discord.Embed(
                description="Ticket Closed!",
                color=discord.Color.red(),
            ),
            view=DeleteTicket()
        )
