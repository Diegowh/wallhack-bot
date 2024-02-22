import asyncio

from discord.ext import commands

from src.server_data import ServerData
from src.bot_state import BotState
import src.settings as settings
from src.utils import validate_map_number


class ServerScanner(commands.Cog):

    def __init__(self, bot, bot_state: BotState):
        self.bot = bot
        self.server_data = ServerData()
        self.bot_state = bot_state

    @commands.command()
    async def pop(self, ctx, map_number):

        if not await validate_map_number(ctx, map_number):
            return

        pop_msg = await self.server_data.pop(map_number)

        await ctx.send(embed=pop_msg)

    @commands.command()
    async def status(self, ctx, map_number):
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

            if not await self.server_data.is_server_down(map_number):
                await ctx.send(f"{role} {map_number} is up!")
                server_command_state["maps"].remove(map_number)
                server_command_state["running"] = False
                print(f"{map_number} status: Online")
                break

            # Server is still down
            counter += 1
            print(f"{map_number} status: Down - {counter}")
            await asyncio.sleep(settings.status_sleep_interval)

    @commands.command(name="autopop")
    async def autopop(self, ctx, arg: str):
        command_name = "autopop"
        # TODO: For now, the bot will only use this command for the server 2154. This will be changed in the future if needed.
        map_number = "2154"
        discord_server_id = ctx.guild.id
        server_command_state: dict = self.bot_state.state[discord_server_id][command_name]

        if arg.lower() == "on":

            # Check if there is another instance of the command running
            if server_command_state["running"]:
                await ctx.send("I'm already running :rage: ")
                return

            server_command_state["running"] = True
            last_msg = None  # This will be used to avoid spamming
            while server_command_state["running"]:

                pop_message = await self.server_data.pop(map_number)

                if last_msg is not None:
                    await last_msg.edit(embed=pop_message)
                else:
                    last_msg = await ctx.send(embed=pop_message)

                # I use this method to allow the bot to be stopped while it's running because. I have to change the way this works.
                for _ in range(settings.autopop_sleep_interval):
                    await asyncio.sleep(1)
                    if not server_command_state["running"]:
                        break

        elif arg.lower() == "off":

            if server_command_state["running"]:
                server_command_state["running"] = False
                await ctx.send("Autopop off!")

        else:
            await ctx.send("Invalid argument. Use /help for more information.")
