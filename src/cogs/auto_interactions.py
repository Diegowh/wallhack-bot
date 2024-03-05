from discord.ext import commands
import discord
from utils import MENTION_RESPONSES
import random

class AutoInteractions(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.bot.user.mentioned_in(message):
            response = random.choice(MENTION_RESPONSES)
            await message.channel.send(f'{message.author.mention} {response}')


async def setup(bot: commands.Bot):
    await bot.add_cog(AutoInteractions(bot))