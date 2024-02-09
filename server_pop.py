import requests


class ServerData:
    def __init__(self, server_id=24295154):
        self.server_id = server_id
        self.url = f"https://api.battlemetrics.com/servers/{
            self.server_id}"

        self.data = self.get_data()

    def get_data(self) -> dict:
        response = requests.get(self.url).json()
        data = response.get("data")
        return data

    def pop(self):
        data = self.get_data()
        players = data.get("attributes").get("players")
        return f"{players}/70 Players on Server"
