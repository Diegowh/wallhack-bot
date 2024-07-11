from __future__ import annotations

import asyncio
import time

import colorama
from colorama import Fore, Back, Style

from config.config import (
    DEVELOPMENT_BOT_TOKEN,
)
from core.bot import Bot
from utils import setup_logging, BOT_SHUT_DOWN_MESSAGE


async def main():

    discord.utils.setup_logging()
    async with Bot() as bot:
        await bot.start(PRODUCTION_BOT_TOKEN, reconnect=True)


if __name__ == '__main__':
    asyncio.run(main())
