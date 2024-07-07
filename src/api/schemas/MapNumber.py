from exceptions.exceptions import (
    InvaidMapNumberTypeError,
    NonDigitMapNumberError,
    InvalidMapNumberLengthError,
    MapNumberStartsWithZeroError,
)
from pydantic import BaseModel, field_validator


class MapNumber(BaseModel):
    """
    Validates if the input is a valid map number for ARK server names.
    """
    num: str
    
    @field_validator("num")
    def valid_map_number(cls, value):
        if not isinstance(value, str):
            raise InvaidMapNumberTypeError("Map number must be a string")
        if not value.isdigit():
            raise NonDigitMapNumberError("Map number must be a digit")
        if len(value) != 4:
            raise InvalidMapNumberLengthError("Map number must be 4 digits long")
        if value[0] == "0":
            raise MapNumberStartsWithZeroError("Map number cannot start with 0")
        return value
