from base64 import b64encode
from typing import Dict, Any

import aiohttp

from src.config.config import (
    CLIENT_ID,
    CLIENT_SECRET,
    DEPLOYMENT_ID,
    EPIC_API,
)
from src.exceptions.exceptions import (
    MapNumberStartsWithZeroError,
    NonDigitMapNumberError,
    InvalidMapNumberLengthError
)


class EpicGamesQuerier:
    def __init__(self) -> None:
        # OAuth2 credentials extracted from ARK: Survival Ascended files
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.deployment_id = DEPLOYMENT_ID
        self.epic_api = EPIC_API
        self.access_token = None

    async def _get_client_access_token(self):
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

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=url,
                headers=headers,
                data=body,
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.access_token = data.get("access_token")

                else:
                    print(f"Failed to obtain access token: {await response.text()}")

    async def _query_info(self, map_number: str):
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
                    'key': 'attributes.CUSTOMSERVERNAME_s',
                    'op': 'CONTAINS',
                    'value': map_number
                },
                {
                    'key': 'attributes.OFFICIALSERVER_s',
                    'op': 'EQUAL',
                    'value': '1'  # Ensure the server is an official one
                }
                # Add other relevant criteria as needed
            ]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=url,
                headers=headers,
                json=payload,
            ) as response:

                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Failed to query server information> {await response.text()}")
                    return None

    async def fetch(self, map_number: str) -> Dict[str, Any]:
        """
        Fetch server information using the Epic Games API.
        """
        if not map_number.isdigit():
            raise NonDigitMapNumberError

        if not len(map_number) == 4:
            raise InvalidMapNumberLengthError

        if map_number.startswith("0"):
            raise MapNumberStartsWithZeroError

        await self._get_client_access_token()
        return await self._query_info(map_number)
