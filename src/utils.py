from enum import StrEnum
from typing import Any


class CommandName(StrEnum):
    AUTOPOP = "autopop"
    POP = "pop"
    STATUS = "status"
    HELP = "help"

    @classmethod
    def _missing_(cls, value) -> Any:
        value = value.lower()
        for member in cls:
            if member == value:
                return member
        return None

class BotTokenName(StrEnum):
    PRODUCTION = "PRODUCTION_BOT_TOKEN"
    DEVELOPMENT = "DEVELOPMENT_BOT_TOKEN"

    @classmethod
    def _missing_(cls, value) -> Any:
        value = value.upper()
        for member in cls:
            if member == value:
                return member
            
            
class AutopopArg(StrEnum):
    ON = "on"
    OFF = "off"
    
    @classmethod
    def _missing_(cls, value) -> Any:
        value = value.lower()
        for member in cls:
            if member == value:
                return member
        return None

async def is_valid_map_number(number) -> bool:
    if number.isdigit() and len(str(number)) == 4:
        return True
    return False
