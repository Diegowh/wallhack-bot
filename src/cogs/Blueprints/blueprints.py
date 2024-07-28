import discord
from discord import app_commands
from src.views.select_blueprint_category import SelectBlueprintCategory
from discord.ext import commands
from src.utils import CommandName
from src.core.image_loader import ImageLoader


class Blueprints(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.view = SelectBlueprintCategory()
        self.blueprint_items = self.view.blueprint_items
        self.selected_blueprint: str | None = None
        self.image_loader = ImageLoader()

    @app_commands.command(
        name=CommandName.BP,
        description="Press enter to select a category, or provide a specific item to get its blueprints."
    )
    @app_commands.describe(item="Item to get its blueprints (optional)")
    async def bp(self, interaction: discord.Interaction, item: str = None):

        if item:
            await self.show_blueprints(interaction=interaction, item=item)
        else:
            await self.show_categories(interaction=interaction)

    async def show_blueprints(self, interaction: discord.Interaction, item: str):
        item = item.lower()
        for category, bp_list in self.blueprint_items.items():
            if item in bp_list:
                self.selected_blueprint = f"{category}_{item}"
                image_files = self.image_loader.get_item_images(category, item)

                await interaction.response.send_message(
                    f"{item.capitalize()} blueprints.",
                    files=image_files,
                    ephemeral=True
                )
                return
        await interaction.response.send_message(
            f"Invalid or unrecognized item provided. \nUse '/bp' to see the blueprint list",
            ephemeral=True
        )

    async def show_categories(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Select a blueprint category",
            view=self.view,
            ephemeral=True,
        )
async def setup(bot: commands.Bot):
    await bot.add_cog(Blueprints(bot))






