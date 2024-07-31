import json

import discord


class SelectBlueprintCategory(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.selected_category = None
        self.blueprint_items = self.load_bluprint_items()

    @discord.ui.button(
        label="Dino",
        style=discord.ButtonStyle.primary,
        emoji="🦕"
    )
    async def dino_button(
            self,
            interaction:
            discord.Interaction,
            button: discord.ui.Button
    ):
        self.selected_category = "dino"
        await self.button_callback(interaction)

    @discord.ui.button(
        label="Weapon",
        style=discord.ButtonStyle.primary,
        emoji="⚔️"
    )
    async def weapon_button(
            self,
            interaction:
            discord.Interaction,
            button: discord.ui.Button
    ):
        self.selected_category = "weapon"
        await self.button_callback(interaction)

    @discord.ui.button(
        label="Wearable",
        style=discord.ButtonStyle.primary,
        emoji="🥷"
    )
    async def wearable_button(
            self,
            interaction:
            discord.Interaction,
            button: discord.ui.Button
    ):
        self.selected_category = "wear"
        await self.button_callback(interaction)

    async def button_callback(self, interaction: discord.Interaction):

        items = self.blueprint_items.get(self.selected_category, [])

        embed = discord.Embed(
            title=f"{self.selected_category.capitalize()} blueprints",
            description="\n".join(items),
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @staticmethod
    def load_bluprint_items() -> dict[list[str]]:
        json_path = "src/config/blueprint_items.json"
        with open(json_path, "r") as file:

            return json.load(file)
