from src.api.controllers.EpicGamesServerQuerier import EpicGamesServerQuerier
from src.api.controllers.ServerlistQuerier import ServerlistQuerier
from src.api.schemas.MapNumber import MapNumber
from src.exceptions.exceptions import (
    MapNotFoundError,
    ServerSessionNotFoundError
)


class ARKServer:
    def __init__(self) -> None:
        self.serverlist_querier = ServerlistQuerier()
        self.epic_querier = EpicGamesServerQuerier()
    
    def map_list(self):
        server_maps = self.serverlist_querier.load_map_ips()
        return [map_name for maps in server_maps.values() for map_name in maps]
    
    def maps_by_ip(self, ip: str):
        all_servers = self.serverlist_querier.get_all_server_maps()
        return all_servers.get(ip)
    
    def server_map_list(self):
        return self.serverlist_querier.get_all_server_maps()
    
    def server_ip_list(self):
        return self.serverlist_querier.official_server_box_ips()
    
    async def map_data_by_number(self, number: str):
        map_number = MapNumber(num=number).num  # Validate the map number
        map_ip = None
        map_name = None
        
        # Find the map number
        map_ips = self.serverlist_querier.get_all_server_maps()
        for ip, box_maps in map_ips.items():
            for map in box_maps:
                if map_number in map:
                    map_ip = ip
                    map_name = map
                    break
        
        if not map_ip or not map_name:
            raise MapNotFoundError
        
        server_box_data = await self.epic_querier.fetch(map_ip)
        for session in server_box_data["sessions"]:
            if map_name in session["attributes"]["CUSTOMSERVERNAME_s"]:
                return session

        raise ServerSessionNotFoundError
