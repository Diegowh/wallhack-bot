from discord.ext import commands


class BotState:
    """
    Stores the state of the bot.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.state = {}

    def __str__(self):
        return f"BotState: {self.state}"
    
    def sync(self):
        for guild in self.bot.guilds:
            self.state[guild.id] = {}
            for cog in self.bot.cogs.values():
                for command in cog.get_commands():
                    self.state[guild.id][command.name] = {
                        "running": False,
                        "maps": [],
                    }
                    print(f"Command {command.name} synced in guild {guild.id}.")

