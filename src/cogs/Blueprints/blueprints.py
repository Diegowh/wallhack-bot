import discord
from discord import app_commands
from src.views.select_blueprint_category import SelectBlueprintCategory
from discord.ext import commands

dinos = [
    'Allosaurus',
    'Ankylo',
    'Araneo',
    'Argentavis',
    'Arthropluera',
    'Baryonyx',
    'Basilosaurus',
    'Beelzebufo',
    'Bronto',
    'Carbonemys',
    'Carcha',
    'Carno',
    'Castoroides',
    'Chalicotherium',
    'Daeodon',
    'Diplodocus',
    'Dire Bear',
    'Doedicurus',
    'Dunkleo',
    'Equus',
    'Fasolasuchus',
    'Gallimimus',
    'Giganoto',
    'Gigantoraptor',
    'Hyaenodon',
    'Ichthyo',
    'Iguanodon',
    'Kaprosuchus',
    'Mammoth',
    'Manta',
    'Mantis',
    'Megalania',
    'Meagloceros',
    'Megalodon',
    'Megalosaurus',
    'Megatherium',
    'Mosasaur',
    'Pachy',
    'Pachyrhinosaurus',
    'Paracer',
    'Parasaur',
    'Pelagorins',
    'Plesiosaur',
    'Procoptodon',
    'Ptera',
    'Pulmonoscorpius',
    'Quetz',
    'Raptor',
    'Rex',
    'Rhyniognatha',
    'Sabertooth',
    'Sarco',
    'Spino',
    'Stego',
    'Tapejara',
    'Terror Bird',
    'Therizinosaurus',
    'Thylacoleo',
    'Trike',
    'Tuso',
    'Woolly Rhino',
    'Xiphactinus',
    'Yuty'
]
wearables = [
    'chitin',
    'flak',
    'gasmask',
    'shield',
    'scuba',

]
weapons = [
    'chainsaw',
    'compbow',
    'crossbow',
    'fabby',
    'flamethrower',
    'net launcher',
    'longneck',
    'hatchet',
    'pick',
    'sickle',
    'pike',
    'shotgun',
    'sword',
    'torch',
    'whip',
    'club',
]
categories = [
    'dino',
    'weapon',
    'wear',
]
blueprint_categories = {
    'dino': dinos,
    'weapon': weapons,
    'wearable': wearables,
}


class Blueprints(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="bp", description="Select a category or provide a specific item")
    @app_commands.describe(item="Item to get its blueprints")
    async def bp(self, interaction: discord.Interaction, item: str = None):

        if item:
            item = item.lower()
            for category, bp_list in blueprint_categories.items():
                if item in bp_list:
                    await interaction.response.send_message(f"You provided the item: {item}", ephemeral=True)
                    return
            await interaction.response.send_message(f"Invalid or unrecognized item provided.", ephemeral=True)
        else:
            await interaction.response.send_message(
                "Select a blueprint category",
                view=SelectBlueprintCategory(),
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Blueprints(bot))






