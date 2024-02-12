import requests
import os
from dotenv import load_dotenv


class ServerData:

    def __init__(self):
        load_dotenv()
        self.url = os.getenv("SERVERLIST_URL")

    def get(self) -> list:
        return requests.get(self.url).json()

    def pop(self, server_number: int = 2154) -> str:
        server_list = self.get()

        assert isinstance(server_list, list)

        for server in server_list:
            name = server.get("Name")

            if str(server_number) in name:

                # Obtain and return the server pop formatted
                num_players = server.get("NumPlayers")
                pop_msg = self._pop_message(num_players)
                return pop_msg

    def _pop_message(self, players: int) -> str:
        return f"{players}/70"
