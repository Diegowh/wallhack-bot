from __future__ import annotations
import asyncio
import discord
from core.bot import Bot
from config.config import (
    DEVELOPMENT_BOT_TOKEN,
    PRODUCTION_BOT_TOKEN,
)


async def main():

    discord.utils.setup_logging()
    async with Bot() as bot:
        await bot.start(PRODUCTION_BOT_TOKEN, reconnect=True)


if __name__ == '__main__':
    asyncio.run(main())
