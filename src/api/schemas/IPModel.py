from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress


class IPModel(BaseModel):
    """
    Validate an IPv4 or IPv6 address.
    """
    ip: IPvAnyAddress
