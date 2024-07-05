import time

import discord
from discord.types.embed import Embed

from utils import is_valid_map_number
from api.controllers.ARKServer import ARKServer
from exceptions.exceptions import (
    MapNotFoundError,
    ServerSessionNotFoundError
    )



class ServerData:
    """Gets the data from the ARK servers
    """

    def __init__(self):
        self.ark_server = ARKServer()

    def create_error_embed(self, title, description):
        time_now = f"<t:{int(time.time())}>"
        embed = discord.Embed(
            title=title, color=0xff0000, description=description
        )
        embed.add_field(name="Last update", value=time_now, inline=True)
        return embed

    async def pop(self, map_number: int) -> discord.Embed:
        if not is_valid_map_number(map_number):

            embed = self.create_error_embed(
                title="Invalid map number",
                description="Map number must be a four digit number.",
            )
            return embed

        map_data = await self.fetch_map_data(map_number)

        if map_data is None:

            embed = self.create_error_embed(
                title="Server not found",
                description="Maybe it's down or the map number is wrong."
            )
            return embed

        # Server found, create the embed message
        pop_embed = self.create_pop_message(map_data)
        return pop_embed

    def create_pop_message(self, map_data) -> discord.Embed:

        # At this point self.server_data should have the server data
        map_name = map_data["attributes"]["CUSTOMSERVERNAME_s"]
        players = map_data["totalPlayers"]
        max_players = map_data["settings"]["maxPublicPlayers"]
        time_now = f"<t:{int(time.time())}>"

        embed = discord.Embed(title=map_name, color=0x00ff00)
        embed.add_field(name="Active Players", value=f"{players}/{max_players}", inline=True)
        embed.add_field(name="Last update", value=time_now, inline=True)
        return embed

    async def is_server_down(self, map_number) -> bool:
        server = await self.fetch_map_data(map_number)
        return server is None

    async def fetch_map_data(self, map_number) -> dict | None:

        assert is_valid_map_number(map_number)

        try:
            return self.ark_server.map_data_by_number(map_number)
        except MapNotFoundError or ServerSessionNotFoundError:
            return None
