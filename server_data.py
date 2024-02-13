import requests
import os
import json
from dotenv import load_dotenv


class ServerData:

    def __init__(self):
        load_dotenv()
        self.url = os.getenv("SERVERLIST_URL")

        with open("server_order.json", "r") as f:
            self.server_order = json.load(f)

    def get(self) -> list:
        return requests.get(self.url).json()

    def pop(self, server_number: int = 2154) -> str:
        server_data_list = self.get()

        assert isinstance(server_data_list, list)

        position = self.server_order.get(str(server_number))

        server_data = server_data_list[position]

        self.server_name = server_data.get("Name")

        # Obtain and return the server pop formatted
        num_players = server_data.get("NumPlayers")
        pop_msg = self._pop_message(num_players)
        return pop_msg

    def _pop_message(self, players: int) -> str:
        return f"{players}/70"
