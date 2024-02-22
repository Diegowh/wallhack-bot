async def is_valid_map_number(number) -> bool:
    if number.isdigit() and len(str(number)) == 4:
        return True
    return False
