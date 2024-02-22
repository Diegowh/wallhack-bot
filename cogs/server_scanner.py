from discord.ext import commands
from server_data import ServerData
from bot_state import BotState
import asyncio
import settings


from utils import validate_map_number


class ServerScanner(commands.Cog):

    def __init__(self, bot, bot_state: BotState):
        self.bot = bot
        self.server_data = ServerData()
        self.bot_state = bot_state

    @commands.command()
    async def pop(self, ctx, map_number: int):

        if not await validate_map_number(ctx, map_number):
            return

        pop_msg = self.server_data.pop(map_number)

        await ctx.send(embed=pop_msg)

    @commands.command()
    async def status(self, ctx, map_number: int):
        command_name = "status"
        if not await validate_map_number(ctx, map_number):
            return

        # Gives the discord server id where the command was called
        discord_server_id = ctx.guild.id
        server_command_state: dict = self.bot_state.state[discord_server_id][command_name]

        # Check if the bot is already looking for the requested ARK server status
        if map_number in server_command_state.get("maps"):
            await ctx.send(f"I'm already looking for {map_number} status, wait :rage: ")
            return

        # Add the map to the list because the bot was not looking for it
        server_command_state["maps"].append(map_number)
        server_command_state["running"] = True

        role = f"<@&492494724528340992>"  # @Member role

        await ctx.send(f"Cheching {map_number} status...")

        counter = 0
        while server_command_state.get("running") == True:

            if not self.server_data.is_server_down(map_number):
                await ctx.send(f"{role} {map_number} is up!")
                server_command_state["maps"].remove(map_number)
                server_command_state["running"] = False
                print(f"{map_number} status: Online")
                break

            # Server is still down
            counter += 1
            print(f"{map_number} status: Down - {counter}")
            await asyncio.sleep(settings.status_sleep_interval)
