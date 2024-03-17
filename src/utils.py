from enum import StrEnum
from typing import Any, Union
import time


def _validate_strenum_value(value: str):
    """Raises TypeError if value is not a string
    """
    if not isinstance(value, str):
        raise TypeError(f"Expected string, got {type(value).__name__}")
        
def time_to_unix(addHours: int) -> int:
    return time.time() + addHours*60*60    

class CommandName(StrEnum):
    AUTOPOP = "autopop"
    POP = "pop"
    STATUS = "status"
    HELP = "help"
    SETTINGS = "settings"

    @classmethod
    def _missing_(cls, value: str) -> Any:
        _validate_strenum_value(value)
        value = value.lower()
        for member in cls:
            if member == value:
                return member
        return None


class BotTokenName(StrEnum):
    PRODUCTION = "PRODUCTION_BOT_TOKEN"
    DEVELOPMENT = "DEVELOPMENT_BOT_TOKEN"

    @classmethod
    def _missing_(cls, value: str) -> Any:
        _validate_strenum_value(value)
        value = value.upper()
        for member in cls:
            if member == value:
                return member
            
            
class AutopopArg(StrEnum):
    ON = "on"
    OFF = "off"
    
    @classmethod
    def _missing_(cls, value: str) -> Any:
        _validate_strenum_value(value)
        value = value.lower()
        for member in cls:
            if member == value:
                return member
        return None

# def is_valid_map_number(number: Union[str, int]) -> bool:
#     number = str(number)
#     if number.isdigit() and len(number) == 4:
#         return True
#     return False


def is_valid_map_number(number: Union[str, int]) -> bool:
    if isinstance(number, (str, int)):
        number = str(number)
        if number.isdigit() and len(number) == 4:
            return True
    return False


MENTION_RESPONSES = [
    "who?",
    "stfu retard",
    "kys",
    "didn't ask",
    "idc",
    "802 was better",
    "Cómo?",
    "Gracias"
]
