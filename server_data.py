import requests


class ServerData:
    """Gets the data from the ARK servers
    """

    def __init__(self):
        self.url = "https://cdn2.arkdedicated.com/servers/asa/officialserverlist.json"

    def get(self) -> list:
        response = requests.get(self.url).json()
        assert isinstance(response, list)
        return response

    def pop(self, server_number: int = 2154) -> str:
        server = self._find_server(server_number)

        if server is None:
            return "Server not found"

        # Obtain and return the server pop formatted
        num_players = server.get("NumPlayers")
        pop_msg = self._pop_message(num_players)
        return pop_msg

    def _pop_message(self, players: int) -> str:
        return f"{players}/70"

    def is_server_down(self, server_number: int = 2154) -> bool:
        server = self._find_server(server_number)
        return server is None

    def _find_server(self, server_number: int) -> dict:
        server_list = self.get()

        for server in server_list:
            if str(server_number) in server.get("Name", ""):
                self.name = server.get("Name")
                return server

        return None
