from __future__ import annotations

from typing import Optional, Union

from discord import Colour, Embed as OriginalEmbed

__all__ = (
    "Embed",
)


class Embed(OriginalEmbed):

    def __init__(self, color: Optional[Union[int, Colour]] = Colour.blue(), **kwargs):

        super().__init__(color=color, **kwargs)

    def credits(self) -> Embed:
        super().set_footer(text="Made by Wallhack")
        return self
