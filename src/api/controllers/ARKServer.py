from src.api.controllers.EpicGamesQuerier import EpicGamesQuerier
from src.api.controllers.ServerlistQuerier import ServerlistQuerier
from src.api.schemas.MapNumber import MapNumber
from src.exceptions.exceptions import (
    MapNotFoundError,
    ServerSessionNotFoundError
)


class ARKServer:
    def __init__(self) -> None:
        self.serverlist_querier = ServerlistQuerier()
        self.epic_querier = EpicGamesQuerier()
    
    async def map_list(self):
        server_maps = self.serverlist_querier.load_map_ips()
        return [map_name for maps in server_maps.values() for map_name in maps]
    
    async def maps_by_ip(self, ip: str):
        all_servers = await self.serverlist_querier.get_all_server_maps()
        return all_servers.get(ip)
    
    async def server_map_list(self):
        return await self.serverlist_querier.get_all_server_maps()
    
    async def server_ip_list(self):
        return await self.serverlist_querier.official_server_box_ips()
    
    async def map_data_by_number(self, number: str):
        map_number = MapNumber(num=number).num  # Validate the map number
        map_ip = None
        map_name = None
        
        # Find the map number
        map_ips = await self.server_map_list()
        for ip, box_maps in map_ips.items():
            for map_ in box_maps:
                if map_number in map_:
                    map_ip = ip
                    map_name = map_
                    break
        
        if not map_ip or not map_name:
            raise MapNotFoundError

        server_box_data = await self.epic_querier.fetch(map_ip)
        for session in server_box_data["sessions"]:
            if map_name in session["attributes"]["CUSTOMSERVERNAME_s"]:
                return session

        raise ServerSessionNotFoundError
