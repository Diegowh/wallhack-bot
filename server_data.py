import requests
import discord
from utils import validate_map_number


class ServerData:
    """Gets the data from the ARK servers
    """

    def __init__(self):
        self.url = "https://cdn2.arkdedicated.com/servers/asa/officialserverlist.json"

    def get(self) -> list:
        response = requests.get(self.url).json()
        assert isinstance(response, list)
        return response

    def pop(self, map_number) -> discord.Embed:
        server = self._find_server(map_number)

        if server is None:
            return "Server not found"

        # Build the message
        pop_msg = self._pop_message()
        return pop_msg

    def _pop_message(self) -> discord.Embed:

        # At this point self.server_data should have the server data
        players = self.server_data.get("NumPlayers")
        max_players = self.server_data.get("MaxPlayers")

        embed = discord.Embed(title=self.name, color=0x00ff00)
        embed.add_field(name="Active Players", value=f"{
                        players}/{max_players}", inline=True
                        )
        return embed

    def is_server_down(self, map_number) -> bool:
        server = self._find_server(map_number)
        return server is None

    def _find_server(self, map_number) -> dict:

        assert validate_map_number(map_number)

        server_list = self.get()

        for server in server_list:
            if map_number in server.get("Name"):
                self.server_data = server
                self.name = server.get("Name")
                return server

        return None
