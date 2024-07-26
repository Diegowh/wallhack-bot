# MapNumber exceptions
class InvalidMapNumberError(Exception):
    """Base exception class"""
    
    def __init__(self, message: str = "Incorrect Map Number") -> None:
        self.message = message
        super().__init__(self.message)
        
        
class InvalidMapNumberTypeError(InvalidMapNumberError):
    """Invalid map number type"""
    pass


class NonDigitMapNumberError(InvalidMapNumberError):
    """Map number is not a digit"""
    pass


class InvalidMapNumberLengthError(InvalidMapNumberError):
    """Map number is not 4 digits long"""
    pass


class MapNumberStartsWithZeroError(InvalidMapNumberError):
    """Map number starts with 0"""
    pass


# IPModel exceptions
class InvalidIPvAnyAddressError(Exception):
    def __init__(self, message: str = "Value is not a valid IPv4 or IPv6 address", name: str = "IPModel") -> None:
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)
        

class MapNotFoundError(Exception):
    def __init__(self, message: str = "Map not found"):
        self.message = message
        super().__init__(self.message)
        
        

class ExceptionHandlerRegistrationError(Exception):
    def __init__(self, message: str = "Error registering exception handlers") -> None:
        super().__init__(message)
        

class ServerSessionNotFoundError(Exception):
    def __init__(self, message: str = "Server session not found"):
        self.message = message
        super().__init__(self.message)

