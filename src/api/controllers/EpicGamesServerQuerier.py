from base64 import b64encode

import requests
from config.config import (
    CLIENT_ID,
    CLIENT_SECRET,
    DEPLOYMENT_ID,
    EPIC_API,
)

from .Querier import Querier


class EpicGamesServerQuerier(Querier):
    def __init__(self) -> None:
        # OAuth2 credentials extracted from ARK: Survival Ascended files
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.deployment_id = DEPLOYMENT_ID
        self.epic_api = EPIC_API
        self.access_token = None


    def get_client_access_token(self):
        url = f"{self.epic_api}/auth/v1/oauth/token"
        auth = b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'deployment_id': self.deployment_id
        }
        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 200:
            self.access_token = response.json().get('access_token')
        else:
            print(f"Failed to obtain access token: {response.text}")

    def _query_info(self, ip_address):
        """
        Query server information using the Epic Games API.
        """
        if not self.access_token:
            print("Access token is not available.")
            return None

        url = f"{self.epic_api}/matchmaking/v1/{self.deployment_id}/filter"
        headers = {
            'Authorization': f"Bearer {self.access_token}",
            'Content-Type': 'application/json'
        }
        
        payload = {
            'criteria': [
                {
                    'key': 'attributes.ADDRESS_s',
                    'op': 'EQUAL',
                    'value': ip_address  # Use the ip_address parameter
                }
                # Add other relevant criteria as needed
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()  # Process this as needed
        else:
            print(f"Failed to query server information: {response.text}")
            return None
    
    def fetch(self, ip):
        """
        Fetch server information using the Epic Games API.
        """
        self.get_client_access_token()
        return self._query_info(ip)
