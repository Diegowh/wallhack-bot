async def validate_map_number(ctx, number) -> bool:
    if number.isdigit() and len(str(number)) == 4:
        return True

    await ctx.send("Map number must be a four digit number.")
    return False
