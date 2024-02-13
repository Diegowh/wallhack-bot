import requests
import os
import re
from dotenv import load_dotenv
import json


class ServerOrderUpdater:
    def __init__(self) -> None:
        load_dotenv()
        self.url = os.getenv("SERVERLIST_URL")

    def update(self):
        server_dict = self._get_server_dict()

        with open("server_order.json", "w") as f:
            json.dump(server_dict, f, indent=4)

    def _get_server_dict(self):
        response = requests.get(self.url).json()
        assert isinstance(response, list)

        server_dict = {self._extract_number(server.get(
            "Name")): i for i, server in enumerate(response)}

        return server_dict

    def _extract_number(self, server_name):
        match = re.search(r'\d+', server_name)
        return int(match.group()) if match else None


if __name__ == "__main__":
    updater = ServerOrderUpdater()
    updater.update()
