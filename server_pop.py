import requests
import os
from dotenv import load_dotenv


class ServerData:

    def __init__(self):
        load_dotenv()
        self.url = os.getenv("SERVERLIST_URL")

    def get(self) -> list:
        return requests.get(self.url).json()

    def pop(self, server_number: int):
        server_list = self.get()

        assert isinstance(server_list, list)

        for server in server_list:
            name = server.get("Name")

            if str(server_number) in name:
                return server.get("NumPlayers")
