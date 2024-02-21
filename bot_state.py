from discord.ext import commands


class BotState:
    """
    Stores the state of the bot.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.state = {}

    def sync(self):
        for cog in self.bot.cogs.values():
            for command in cog.get_commands():
                self.state[command.name] = False
                print(f"Command {command.name} synced.")
