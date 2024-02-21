from discord.ext import commands
from server_data import ServerData
from bot_state import BotState

from utils import validate_server_number


class ServerScanner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_data = ServerData()

        # Key: discord server id, Value: list of Ark server numbers
        self.running_status_in_servers = {}
        self.running_autpop_in_servers = set()
        

    @commands.command()
    async def pop(self, ctx, server_number: int):

        if not await validate_server_number(ctx, server_number):
            return

        pop_msg = self.server_data.pop(server_number)

        await ctx.send(embed=pop_msg)
