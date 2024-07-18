from src.views import *
from src.views.close_ticket import CloseTicket


class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary, emoji="📩", custom_id="create_ticket")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer(ephemeral=True)
        category: discord.CategoryChannel = discord.utils.get(
            interaction.guild.categories,
            id=OPENED_TICKETS_CATEGORY_ID,
        )
        for channel in category.text_channels:
            if channel.topic == f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!":
                await interaction.followup.send(
                    f"You already have a ticket in {channel.mention}",
                    ephemeral=True
                )
                return

        role: discord.Role = interaction.guild.get_role(MEMBER_ROLE_ID)
        overwrites = {
            # interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            role: discord.PermissionOverwrite(
                view_channel=False,
                read_messages=False,
                send_messages=False,
                manage_messages=False
            ),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                read_messages=True,
                send_messages=True
            ),
        }

        channel = await category.create_text_channel(
            name=interaction.user.name,
            topic=f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL!",
            overwrites=overwrites,
        )

        await channel.send(
            embed=discord.Embed(
                title="Ticket Created!",
                description="Don't ping a staff member, they will be here soon.",
                color=discord.Color.green()
            ),
            view=CloseTicket()
        )

        await interaction.followup.send(
            embed=discord.Embed(
                description=f"Created your ticket in {interaction.channel.mention}",
                color=discord.Color.blurple()
            ),
            ephemeral=True
        )

        await send_log(
            title="Ticket created",
            description=f"Created by {interaction.user.mention}",
            color=discord.Color.green(),
            guild=interaction.guild
        )