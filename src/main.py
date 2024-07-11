from __future__ import annotations

import asyncio

import discord

from config.config import (
    PRODUCTION_BOT_TOKEN,
    DEVELOPMENT_BOT_TOKEN,
)
from core.bot import Bot


async def main():

    discord.utils.setup_logging()
    async with Bot() as bot:
        await bot.start(PRODUCTION_BOT_TOKEN, reconnect=True)


if __name__ == '__main__':
    asyncio.run(main())
