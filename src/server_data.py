import time
import requests

import discord

from utils import is_valid_map_number


class ServerData:
    """Gets the data from the ARK servers
    """

    def __init__(self):
        self.url = "https://cdn2.arkdedicated.com/servers/asa/officialserverlist.json"

    def get(self) -> list:
        response = requests.get(self.url).json()
        assert isinstance(response, list)
        return response

    async def pop(self, map_number) -> discord.Embed:
        if not await is_valid_map_number(map_number):
            time_now = f"<t:{int(time.time())}>"
            invalid_num_msg = discord.Embed(title="Invalid map number", color=0xff0000,
                                            description="Map number must be a four digit number.")
            invalid_num_msg.add_field(name="Last update",
                                      value=time_now, inline=True)
            return invalid_num_msg

        server = await self._find_server(map_number)

        if server is None:
            time_now = f"<t:{int(time.time())}>"

            error_msg = discord.Embed(title="Server not found", color=0xff0000,
                                      description="Maybe it's down or the map number is wrong.")
            error_msg.add_field(name="Last update",
                                value=time_now, inline=True)
            return error_msg

        # Server found, create the embed message
        pop_msg = self._pop_message()
        return pop_msg

    def _pop_message(self) -> discord.Embed:

        # At this point self.server_data should have the server data
        players = self.server_data.get("NumPlayers")
        max_players = self.server_data.get("MaxPlayers")
        time_now = f"<t:{int(time.time())}>"

        embed = discord.Embed(title=self.name, color=0x00ff00)
        embed.add_field(name="Active Players", value=f"{
                        players}/{max_players}", inline=True
                        )
        embed.add_field(name="Last update", value=time_now, inline=True)
        return embed

    async def is_server_down(self, map_number) -> bool:
        server = await self._find_server(map_number)
        return server is None

    async def _find_server(self, map_number) -> dict:

        assert await is_valid_map_number(map_number)

        server_list = self.get()

        for server in server_list:
            if map_number in server.get("Name"):
                self.server_data = server
                self.name = server.get("Name")
                return server

        return None
