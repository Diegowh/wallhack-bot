import json
from typing import Dict, Any, List

import aiohttp
import asyncio
from src.config.config import SERVERLIST_URL

from src.api.controllers.Querier import Querier


class ServerlistQuerier:
    """
    Class to fetch ARK: Survival Ascended official server list data.
    """
    def __init__(self) -> None:
        self.official_server_list_url = SERVERLIST_URL
    
    async def fetch(self) -> list[dict] | None:
        """
        Fetches the official server list data.
        """
        url = self.official_server_list_url
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Failed to fetch official server data: {response.status}")
                        return None

        except aiohttp.ClientConnectorError as e:
            print(f"Connection error: {e}")

    async def official_server_box_ips(self) -> set[str]:
        """Returns a set of all official server IPs."""
        response = await self.fetch()
        return {server["IP"] for server in response}

    async def get_all_server_maps(self) -> dict[Any, list[Any]]:
        """Returns a dictionary of server IPs and their respective maps."""
        map_ips = {}
        all_ips = await self.official_server_box_ips()
        server_list_data = await self.fetch()
        for server_data in server_list_data:
            ip = server_data["IP"]
            if ip in all_ips:
                if ip not in map_ips:
                    map_ips[ip] = []
                map_ips[ip].append(server_data["Name"])
        return map_ips

    def save_or_update_map_ips(self) -> None:
        """Saves or updates the map IPs to a JSON file."""
        map_ips = self.load_map_ips()
        with open("map_ips.json", "w") as f:
            json.dump(map_ips, f, indent=4)

    @staticmethod
    def load_map_ips() -> dict:
        """Loads the map IPs from a JSON file."""
        with open("map_ips.json", "r") as f:
            return json.load(f)