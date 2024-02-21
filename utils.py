async def validate_server_number(ctx, number: int) -> bool:
    if not isinstance(number, int):
        await ctx.send("Server number must be a four digit number.")
        return False
    return True
