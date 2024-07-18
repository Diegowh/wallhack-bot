# import discord
# from typing import Any
#
#
# class BlueprintCategories(discord.ui.Select):
#     def __init__(self, parent):
#         self.parent = parent
#         options = [
#             discord.SelectOption(label="Dino Blueprints", value="dino"),
#             discord.SelectOption(label="Weapon Blueprints", value="weapon"),
#             discord.SelectOption(label="Wearables", value="wear"),
#         ]
#         super().__init__(placeholder="Select a blueprint category", options=options)
#
#     async def callback(self, interaction: discord.Interaction) -> Any:
#         selected_category = self.values[0]
#         await interaction.response.send_message(
#             f"You have selected {selected_category}",
#             ephemeral=True
#         )
