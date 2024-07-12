from __future__ import annotations

import asyncio
from utils import get_current_branch
import colorama

from config.config import (
    PRODUCTION_BOT_TOKEN,
    DEVELOPMENT_BOT_TOKEN
)
from core.bot import Bot
from utils import setup_logging, BOT_SHUT_DOWN_MESSAGE


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
