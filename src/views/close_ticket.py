from src.views import *
from src.views.delete_ticket import DeleteTicket


class CloseTicket(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close the ticket", style=discord.ButtonStyle.red, custom_id="close_ticket", emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send("Closing this ticket in 3 seconds!")
        await asyncio.sleep(3)

        closed_category: discord.CategoryChannel = discord.utils.get(
            interaction.guild.categories,
            id=CLOSED_TICKETS_CATEGORY_ID
        )
        member_role: discord.Role = interaction.guild.get_role(MEMBER_ROLE_ID)

        ticket_creator_id = int(interaction.channel.topic.split()[0])
        ticket_creator = interaction.guild.get_member(ticket_creator_id)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, manage_messages=False),
            ticket_creator: discord.PermissionOverwrite(read_messages=True, send_messages=False, manage_messages=False)
        }
        await interaction.channel.edit(category=closed_category, overwrites=overwrites)
        await interaction.channel.send(
            embed=discord.Embed(
                description="Ticket Closed!",
                color=discord.Color.red(),
            ),
            view=DeleteTicket()
        )

        await send_log(
            title="Ticket closed",
            description=f"Closed by {interaction.user.mention}\n",
            color=discord.Color.yellow(),
            guild=interaction.guild
        )
