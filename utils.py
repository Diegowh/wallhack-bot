async def validate_map_number(number, ctx=None) -> bool:
    if number.isdigit() and len(str(number)) == 4:
        return True

    if ctx is not None:
        await ctx.send("Map number must be a four digit number.")

    return False
