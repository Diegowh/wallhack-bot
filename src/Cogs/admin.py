from discord.ext import commands
import discord
from src import settings


class Admin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

