from . import *


class DeleteTicket(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Delete the ticket", style=discord.ButtonStyle.red, emoji="🚮", custom_id="delete_ticket")
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer()
        await interaction.channel.send("Deleting the ticket in 3 seconds")
        await asyncio.sleep(3)

        await interaction.channel.delete()
