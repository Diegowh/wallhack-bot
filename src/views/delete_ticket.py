import discord

from src.views import *


class DeleteTicket(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Delete the ticket", style=discord.ButtonStyle.red, emoji="🚮", custom_id="delete_ticket")
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):

        ticket_creator_id = int(interaction.channel.topic.split()[0])
        if interaction.user.id == ticket_creator_id:
            await interaction.response.send_message(f"{interaction.user.mention}, you cannot delete this ticket.")
            return

        await interaction.response.defer()
        await interaction.channel.send("Deleting the ticket in 3 seconds")
        await asyncio.sleep(3)

        await interaction.channel.delete()

        await send_log(
            title="Ticket deleted",
            description=f"Ticket '{interaction.channel.name}' deleted by {interaction.user.mention}.",
            color=discord.Color.red(),
            guild=interaction.guild,
        )