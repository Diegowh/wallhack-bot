import asyncio
import time

from discord.ext import commands

from src.server_data import ServerData
from src.utils import CommandName, AutopopArg


class ServerScanner(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.settings = self.bot.settings
        self.server_data = ServerData()
        self.autopop_task = None

    async def delete_previous_messages(self, ctx: commands.Context, limit):
        async for message in ctx.channel.history(limit=limit):
            if message.id != self.settings.autopop_to_preserve_msg_id:
                await message.delete()

    @commands.command(name=CommandName.POP)
    async def pop(self, ctx: commands.Context, map_number):

        pop_msg = await self.server_data.pop(map_number)

        await ctx.send(embed=pop_msg)

    def __get_server_command_state(self, ctx: commands.Context) -> dict:
        command_name = ctx.command.name
        # Gives the discord server id where the command was called
        discord_server_id = ctx.guild.id
        return self.bot.state.state[discord_server_id][command_name]

    async def __run_status_task(self, ctx: commands.Context, map_number, server_command_state: dict):
        while server_command_state.get("running"):

            if not await self.server_data.is_server_down(map_number):

                # Server is still up (maybe wrong command use or the server is still showing)

                await ctx.send(f"{self.settings.role_to_tag} {map_number} is up!")
                server_command_state["maps"].remove(map_number)
                server_command_state["running"] = False
                print(f"{map_number} status: Online")
                break

            # Server is still down
            await asyncio.sleep(self.settings.status_sleep_interval)

    @commands.command(name=CommandName.STATUS)
    async def status(self, ctx: commands.Context, map_number):
        server_command_state = self.__get_server_command_state(ctx)

        # Check if the bot is already looking for the requested ARK server status
        if map_number in server_command_state.get("maps"):
            await ctx.send(f"I'm already looking for {map_number} status, wait :rage: ")
            return

        # Add the map to the list because the bot was not looking for it
        server_command_state["maps"].append(map_number)
        server_command_state["running"] = True

        await ctx.send(f"Checking {map_number} status...")

        # Check when command is called if the server is still up
        await self.__wait_for_server_down(ctx, map_number, server_command_state)

        # previous_server_state = "down" if await self.server_data.is_server_down(map_number) else "up"

        await self.__run_status_task(ctx, map_number, server_command_state)

    @commands.command(name=CommandName.AUTOPOP)
    async def autopop(self, ctx: commands.Context, arg: str):
        command_name = ctx.command.name
        discord_server_id = ctx.guild.id
        server_command_state: dict = self.bot.state.state[discord_server_id][command_name]

        if arg.lower() == AutopopArg.ON:
            await self.run_autopop(ctx, server_command_state)

        elif arg.lower() == AutopopArg.OFF:
            await self.stop_autopop(ctx, server_command_state)

        else:
            await ctx.send("Invalid argument. Use /help for more information.")
    # Methods

    async def run_autopop(self, ctx: commands.Context, state: dict):

        # Check if there is another instance of the command running
        if state["running"]:
            await ctx.send("I'm already running :rage: ")
            return

        state["running"] = True

        # Get last msg in the channel sent by the bot to delete it.
        await self.delete_previous_messages(ctx, limit=100)

        # Run the task
        self.autopop_task = asyncio.create_task(
            self.__autopop_task(ctx, state)
        )

    async def __autopop_task(self, ctx: commands.Context, state: dict):
        last_msg = None  # Im using this just to avoid spamming the channel
        while state["running"]:

            pop_message = await self.server_data.pop(self.settings.autopop_main_map)

            if last_msg is not None:
                await last_msg.edit(embed=pop_message)
            else:
                last_msg = await ctx.send(embed=pop_message)

            await asyncio.sleep(self.settings.autopop_sleep_interval)

    async def stop_autopop(self, ctx: commands.Context, state: dict):

        if state["running"]:
            await self.delete_previous_messages(ctx, limit=100)
            self.autopop_task.cancel()
            state["running"] = False
            await ctx.send("Autopop off!")

    async def __wait_for_server_down(self, ctx: commands.Context, map_number, server_command_state: dict):

        if not await self.server_data.is_server_down(map_number):
            start_time = time.time()
            while time.time() - start_time < self.settings.status_timeout:
                await asyncio.sleep(self.settings.status_sleep_interval)
                if await self.server_data.is_server_down(map_number):
                    break

            else:
                # Server is still up after the timeout
                await ctx.send(f"{map_number} is still up, please try again.")
                server_command_state["maps"].remove(map_number)
                server_command_state["running"] = False
                return

    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to provide a map number.")
        else:
            raise error


async def setup(bot: commands.Bot):
    await bot.add_cog(ServerScanner(bot))
