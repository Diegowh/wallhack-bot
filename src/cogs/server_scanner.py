import asyncio
import time

from discord.ext import commands

import settings as settings
from server_data import ServerData
from bot_state import BotState
from utils import CommandName, AutopopArg


class ServerScanner(commands.Cog):

    def __init__(self, bot: commands.Bot, bot_state: BotState):
        self.bot = bot
        self.server_data = ServerData()
        self.bot_state = bot_state

    @commands.command(name=CommandName.POP)
    async def pop(self, ctx: commands.Context, map_number):

        pop_msg = await self.server_data.pop(map_number)

        await ctx.send(embed=pop_msg)

    @commands.command(name=CommandName.STATUS)
    async def status(self, ctx: commands.Context, map_number):
        command_name = ctx.command.name

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

        await ctx.send(f"Cheching {map_number} status...")

        # Check when command is called if the server is still up
        await self.wait_for_server_down(ctx, map_number, server_command_state)

        # previous_server_state = "down" if await self.server_data.is_server_down(map_number) else "up"
        counter = 0

        while server_command_state.get("running") == True:

            if not await self.server_data.is_server_down(map_number):

                # Server is still up (maybe wrong command use or the server is still showing)

                await ctx.send(f"{settings.role_to_tag} {map_number} is up!")
                server_command_state["maps"].remove(map_number)
                server_command_state["running"] = False
                print(f"{map_number} status: Online")
                break

            # Server is still down
            counter += 1
            print(f"{map_number} status: Down - {counter}")
            await asyncio.sleep(settings.status_sleep_interval)

    @commands.command(name=CommandName.AUTOPOP)
    async def autopop(self, ctx: commands.Context, arg: str):
        command_name = ctx.command.name
        discord_server_id = ctx.guild.id
        server_command_state: dict = self.bot_state.state[discord_server_id][command_name]

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

            pop_message = await self.server_data.pop(settings.autopop_main_map)

            if last_msg is not None:
                await last_msg.edit(embed=pop_message)
            else:
                last_msg = await ctx.send(embed=pop_message)

            await asyncio.sleep(settings.autopop_sleep_interval)

    async def stop_autopop(self, ctx: commands.Context, state: bool):

        if state["running"]:
            
            # Delete the last message sent by the bot
            await self.delete_previous_messages(ctx, limit=100)

            self.autopop_task.cancel()
            state["running"] = False
            await ctx.send("Autopop off!")

    async def delete_previous_messages(self, ctx: commands.Context, limit):
        async for message in ctx.channel.history(limit=limit):
            if message.id != settings.autopop_to_preserve_msg_id:
                await message.delete()

    async def wait_for_server_down(self, ctx: commands.Context, map_number, server_command_state: dict):
        
        if not await self.server_data.is_server_down(map_number):
            start_time = time.time()
            while time.time() - start_time < settings.status_timeout:
                await asyncio.sleep(settings.status_sleep_interval)
                if await self.server_data.is_server_down(map_number):
                    break

            else:
                # Server is still up after the timeout
                await ctx.send(f"{map_number} is still up, please try again.")
                server_command_state["maps"].remove(map_number)
                server_command_state["running"] = False
                return