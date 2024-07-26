import time
from typing import Optional, Dict, Any

import discord

from src.api.controllers.EpicGamesQuerier import EpicGamesQuerier
from src.exceptions.exceptions import InvalidMapNumberError


class ARKDataManager:

    def __init__(self):
        self.querier = EpicGamesQuerier()

    async def get_embed(self, map_number: str) -> discord.Embed:
        try:
            data = await self.querier.fetch(map_number)
        except InvalidMapNumberError:
            return self._invalid_input_embed()
        except Exception:
            return self._generic_error_embed()
        return self._create_embed(data)

    @staticmethod
    def _create_embed(data: Optional[Dict[str, Any]]) -> discord.Embed:

        if data:
            data = data['sessions'][0]
            last_update = data['lastUpdated'] = int(time.time())
            map_name = data["attributes"]["CUSTOMSERVERNAME_s"]
            current_players = data['totalPlayers']
            max_players = data['settings']['maxPublicPlayers']

            embed = discord.Embed(
                title=f"{map_name}\n",
                description=f"---------------------------------------\n"
                      f"👥 **Current Players:** {current_players}/{max_players}\n\n"
                      f"🕒 **Last Updated:** <t:{last_update}:R>\n"
                      f"---------------------------------------",
                color=0x00ff00,
            )
            return embed

        time_now = int(time.time())
        embed = discord.Embed(
            title=f"Server not found\n"
                  f"---------------------------------------\n"
                  f"🚫 Server is down\n\n"
                  f"🕒 Last Updated: <t:{time_now}:R>\n"
                  f"---------------------------------------",
            color=0xff0000,
        )
        return embed

    @staticmethod
    def _invalid_input_embed() -> discord.Embed:
        embed = discord.Embed(
            title=f"Invalid Map Number\n"
                  f"---------------------------------------\n"
                  f"🥵 The number provided is incorrect\n"
                  f"---------------------------------------",
            color=0xff0000,
        )
        return embed

    @staticmethod
    def _generic_error_embed() -> discord.Embed:
        embed = discord.Embed(
            title=f"Unexpected Error\n"
                  f"---------------------------------------\n"
                  f"😩 Something went wrong\n\n"
                  f"🙏 Try again\n"
                  f"---------------------------------------",
            color=0xff0000,
        )
        return embed

    async def is_server_down(self, map_number) -> bool:
        response = await self.querier.fetch(map_number)
        return response['count'] == 0
