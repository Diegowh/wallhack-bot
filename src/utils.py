import logging
import subprocess
import time
from enum import StrEnum
from typing import Any, Union

from colorama import Fore, Style


def _validate_strenum_value(value: str):
    """
    Raises TypeError if value is not a string

    Args:
        value (str): Value to be validated

    Raises:
        TypeError: If the value is not a string
    """
    if not isinstance(value, str):
        raise TypeError(f"Expected string, got {type(value).__name__}")


def time_to_unix(addHours: int) -> int:
    return time.time() + addHours * 60 * 60


class CommandName(StrEnum):
    AUTOPOP = "autopop"
    POP = "pop"
    STATUS = "status"
    HELP = "help"
    SETTINGS = "settings"
    CLAIMS = "claims"
    TICKET = "ticket"
    BP = "bp"

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
    """
    Validate if the given number is a valid map number for ARK Official Servers

    Args:
        number (Union[str, int]): The number to be validated

    Returns:
        bool: True if the number is a valid map number, False otherwise
    """
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
    "Gracias",
    "hola",
    "buenos dias",
    "uwu",
    "que te den"
]


class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: f"{Style.BRIGHT}[%(asctime)s]{Fore.BLUE} [%(levelname)s] {Style.RESET_ALL}{Style.BRIGHT}%(message)s",
        logging.INFO: f"{Style.BRIGHT}[%(asctime)s]{Fore.GREEN} [%(levelname)s] {Style.RESET_ALL}{Style.BRIGHT}%(message)s",
        logging.WARNING: f"{Style.BRIGHT}[%(asctime)s]{Fore.YELLOW} [%(levelname)s] {Style.RESET_ALL}{Style.BRIGHT}%(message)s",
        logging.ERROR: f"{Style.BRIGHT}[%(asctime)s]{Fore.RED} [%(levelname)s] {Style.RESET_ALL}{Style.BRIGHT}%(message)s",
        logging.CRITICAL: f"{Style.BRIGHT}[%(asctime)s]{Fore.RED} [%(levelname)s] {Style.RESET_ALL}{Style.BRIGHT}%(message)s"
    }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


def setup_logging():
    logger = logging.getLogger("Bot")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)


BOT_SHUT_DOWN_MESSAGE  = f"{Style.BRIGHT}[{time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}]{Fore.GREEN} [INFO] {Fore.LIGHTWHITE_EX}Bot has been shut down"


def get_current_branch():
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode('utf-8')
        return branch
    except subprocess.CalledProcessError as e:
        print(f"Error while getting the current branch: {e}")
        return None
