import discord

LOGS_CHANNEL_ID = 1260724325556814025


async def send_log(title: str, guild: discord.Guild, description: str, color: discord.Color):
    log_channel = guild.get_channel(LOGS_CHANNEL_ID)
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    await log_channel.send(embed=embed)