from __future__ import annotations

import asyncio

import colorama

from src.config.config import (
    PRODUCTION_BOT_TOKEN,
    DEVELOPMENT_BOT_TOKEN
)
from src.core.bot import Bot
from src.utils import setup_logging, get_current_branch, BOT_SHUT_DOWN_MESSAGE


async def main():
    setup_logging()
    branch = get_current_branch()
    bot_token = PRODUCTION_BOT_TOKEN if branch == "main" else DEVELOPMENT_BOT_TOKEN

    async with Bot() as bot:
        await bot.start(bot_token, reconnect=True)


if __name__ == '__main__':
    colorama.init()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(BOT_SHUT_DOWN_MESSAGE)
