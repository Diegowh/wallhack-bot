import discord

LOGS_CHANNEL_ID = 1261351522227458049


async def send_log(title: str, guild: discord.Guild, description: str, color: discord.Color):
    log_channel = guild.get_channel(LOGS_CHANNEL_ID)
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    await log_channel.send(embed=embed)