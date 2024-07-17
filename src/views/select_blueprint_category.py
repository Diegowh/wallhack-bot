import discord

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
    # 'Equus',
    # 'Fasolasuchus',
    # 'Gallimimus',
    # 'Giganoto',
    # 'Gigantoraptor',
    # 'Hyaenodon',
    # 'Ichthyo',
    # 'Iguanodon',
    # 'Kaprosuchus',
    # 'Mammoth',
    # 'Manta',
    # 'Mantis',
    # 'Megalania',
    # 'Meagloceros',
    # 'Megalodon',
    # 'Megalosaurus',
    # 'Megatherium',
    # 'Mosasaur',
    # 'Pachy',
    # 'Pachyrhinosaurus',
    # 'Paracer',
    # 'Parasaur',
    # 'Pelagorins',
    # 'Plesiosaur',
    # 'Procoptodon',
    # 'Ptera',
    # 'Pulmonoscorpius',
    # 'Quetz',
    # 'Raptor',
    # 'Rex',
    # 'Rhyniognatha',
    # 'Sabertooth',
    # 'Sarco',
    # 'Spino',
    # 'Stego',
    # 'Tapejara',
    # 'Terror Bird',
    # 'Therizinosaurus',
    # 'Thylacoleo',
    # 'Trike',
    # 'Tuso',
    # 'Woolly Rhino',
    # 'Xiphactinus',
    # 'Yuty'
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


class SelectBlueprintCategory(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.selected_category = None

        self.blueprint_categories = {
            'dino': dinos,
            'weapon': weapons,
            'wearable': wearables,
        }

    @discord.ui.select(
        placeholder="Select a blueprint category",
        options=[
            discord.SelectOption(label="Dino Blueprints", value="dino"),
            discord.SelectOption(label="Weapon Blueprints", value="weapon"),
            discord.SelectOption(label="Wearables", value="wear"),
        ],
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):

        self.selected_category = select.values[0]
        await interaction.response.send_message(
            f"You have selected {self.selected_category}.",
            ephemeral=True
        )
        # await interaction.response.defer(ephemeral=True)
        items = self.blueprint_categories.get(self.selected_category)
        for item in items:
            button = discord.ui.Button(label=item)
            button.custom_id = item
            self.add_item(button)

        await interaction.followup.send(
            f"Here are the blueprints for {self.selected_category}: ", view=self, ephemeral=True
        )


