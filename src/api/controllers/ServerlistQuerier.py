import json

import requests
from src.config.config import SERVERLIST_URL

from .Querier import Querier


class ServerlistQuerier(Querier):
    """
    Class to fetch ARK: Survival Ascended official server list data.
    """
    def __init__(self) -> None:
        self.official_server_list_url = SERVERLIST_URL
    
    def fetch(self) -> list[dict] | None:
        """
        Fetches the official server list data.
        """
        url = self.official_server_list_url
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch official server data: {response.text}")
            return None
    
    def official_server_box_ips(self) -> set[str]:
        """Returns a set of all official server IPs."""
        response = self.fetch()
        return {server["IP"] for server in response}

    def get_all_server_maps(self) -> list[dict]:
        """Returns a dictionary of server IPs and their respective maps."""
        map_ips = {}
        all_ips = self.official_server_box_ips()
        server_list_data = self.fetch()
        for server_data in server_list_data:
            ip = server_data["IP"]
            if ip in all_ips:
                if ip not in map_ips:
                    map_ips[ip] = []
                map_ips[ip].append(server_data["Name"])
        return map_ips

    def save_or_update_map_ips(self) -> None:
        """Saves or updates the map IPs to a JSON file."""
        map_ips = self.get_map_ips()
        with open("map_ips.json", "w") as f:
            json.dump(map_ips, f, indent=4)

    def load_map_ips(self) -> dict:
        """Loads the map IPs from a JSON file."""
        with open("map_ips.json", "r") as f:
            return json.load(f)