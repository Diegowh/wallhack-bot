from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
