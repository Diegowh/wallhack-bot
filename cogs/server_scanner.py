from discord.ext import commands
from server_data import ServerData
from bot_state import BotState


class ServerScanner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_data = ServerData()

    @commands.command()
    async def pop(self, ctx, server_number: int):

        if not isinstance(server_number, int):
            await ctx.send("Server number must be a four digit number.")
            return

        pop_msg = self.server_data.pop(server_number)

        await ctx.send(embed=pop_msg)
