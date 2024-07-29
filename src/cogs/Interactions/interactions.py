from __future__ import  annotations

import random

import discord
from discord.ext import commands
from src.core.bot import Bot
from src.utils import MENTION_RESPONSES

class Interactions(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.clown_emoji = "\U0001F921"
        self.hug_emoji = "\U0001FAC2"
        self.concerned_monkey_gif = "https://tenor.com/view/monkey-confused-gif-15712129875520007531"
        self.member_role_id = 492494724528340992

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # if message.author.id == self.bot.id:
        #     return

        # if self.bot.user.mentioned_in(message):
        #
        #     response = random.choice(MENTION_RESPONSES)
        #     await message.channel.send(f'{message.author.mention} {response}')

        # Member
        user_roles = [role.id for role in message.author.roles]
        if self.member_role_id in user_roles:
            if random.random() < 0.005:
                await message.add_reaction(self.clown_emoji)

        # Pablo
        if message.author.id == 495339969758363678:
            if random.random() < 0.2:
                emoji = random.choice([self.clown_emoji, self.hug_emoji])
                await message.add_reaction(emoji)

            if random.random() < 0.05:
                await message.reply(self.concerned_monkey_gif)

        # Alex
        if message.author.id == 314179525820940298:
            if random.random() < 0.02:
                await message.add_reaction("🤫")


async def setup(bot: commands.Bot):
    await bot.add_cog(Interactions(bot))
