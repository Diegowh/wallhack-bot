import asyncio
import time

from discord.ext import commands, tasks
from server_data import ServerData
from utils import CommandName


class ServerScanner(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.settings = self.bot.settings.get("values")
        self.server_data = ServerData()
        self.autopop_task = None

        self.check_status_task = None
        self.server_was_down = False
        self.status_map_number = None
        self.status_ctx = None

    async def delete_previous_messages(self, ctx: commands.Context, limit):
        async for message in ctx.channel.history(limit=limit):
            if message.id != self.settings.get("autopop_to_preserve_msg_id"):
                await message.delete()

    @commands.command(name=CommandName.POP)
    async def pop(self, ctx: commands.Context, map_number):

        pop_msg = await self.server_data.pop(map_number)

        await ctx.send(embed=pop_msg)

    @commands.command(name=CommandName.STATUS)
    async def status(self, ctx: commands.Context, map_number: str):
        self.status_map_number = map_number
        self.status_ctx = ctx

        if self.check_status is not None:
            self.check_status.cancel()

        self.server_was_down = False
        self.check_status.start()

        await ctx.send(f"Started checking status for server {self.status_map_number}...")

        await asyncio.sleep(300)  # Le doy 5 minutos por si ha sido un uso indebido del comando
        if not self.server_was_down:
            await ctx.send(f"The server {map_number} is still up, try again.")
            self.check_status.cancel()

    async def is_server_down(self, map_number) -> bool:
        server = await self.server_data.is_server_down(map_number)
        return server is None

    @tasks.loop(seconds=15)
    async def check_status(self):
        is_down = await self.is_server_down(self.status_map_number)
        if is_down:
            self.server_was_down = True
        elif self.server_was_down:
            member_role = f"<@&{self.settings.get('role_id_to_tag')}>"
            await self.status_ctx.send(f"{member_role} {self.status_map_number} is up!")
            self.check_status.cancel()

    @check_status.before_loop
    async def before_status_task(self):
        await self.bot.wait_until_ready()

    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to provide a map number.")
        else:
            raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(ServerScanner(bot))
