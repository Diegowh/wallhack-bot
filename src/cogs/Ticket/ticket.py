import discord
from discord.ext import commands
from views.create_ticket import CreateTicket

MEMBER_ROLE_ID = 1260548665148444722


class Ticket(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="ticket")
    @commands.has_role(MEMBER_ROLE_ID)
    async def ticket(self, ctx: commands.Context):
        await ctx.send(
            embed=discord.Embed(
                description="Press the button to create a new ticket!"
            ),
            view=CreateTicket()
        )

    @ticket.error
    async def ticket_error(self, ctx: commands.Context, error: commands.CommandError):
        # Evito ensuciar la consola con excepciones ignoradas
        if isinstance(error, commands.MissingRole):
            pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))


