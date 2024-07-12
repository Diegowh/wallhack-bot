import random

import discord
from discord.ext import commands
from utils import MENTION_RESPONSES


class Interactions(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.bot.user.mentioned_in(message):
            response = random.choice(MENTION_RESPONSES)
            await message.channel.send(f'{message.author.mention} {response}')
        if message.author.id == 495339969758363678:  # ID de Pablo
            clown_emoji = "\U0001F921"
            hug_emoji = "\U0001FAC2"
            await message.add_reaction(hug_emoji)


async def setup(bot: commands.Bot):
    await bot.add_cog(Interactions(bot))
