from __future__ import annotations

import datetime
import os
import sqlite3
import time
from typing import TYPE_CHECKING

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from discord import app_commands
from discord.ext import commands

from src.cogs.Timer.utils import TimerData
from src.utils import CommandName

if TYPE_CHECKING:
    from src.core.bot import Bot


class Timer(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.db_path = os.path.join(os.path.dirname(__file__), 'timers.db')
        self.conn = sqlite3.connect(self.db_path)
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.create_table()
        self.load_timers()

    def create_table(self):
        c = self.conn.cursor()
        c.execute(
            '''CREATE TABLE IF NOT EXISTS timers
            (message_id INTEGER, channel_id INTEGER, user_id INTEGER, message TEXT, run_date TIMESTAMP)'''
        )
        self.conn.commit()

    def load_timers(self):
        c = self.conn.cursor()
        c.execute("SELECT message_id, channel_id, user_id, message, run_date FROM timers")
        rows = c.fetchall()
        c.close()
        for row in rows:
            timer_data = TimerData.from_row(row)
            if timer_data.run_date > datetime.datetime.now():
                trigger = DateTrigger(run_date=timer_data.run_date)
                self.scheduler.add_job(self.timer_callback, trigger, args=[timer_data])

            else:
                channel = self.bot.get_channel(timer_data.channel_id)
                if channel:
                    self.bot.loop.create_task(channel.send(f"Sorry <@{timer_data.user_id}>, the timer: **{timer_data.message}** has expired "
                                                           f"while the bot was down."))
                    self.delete_timer(timer_data.message_id)
    
    def delete_timer(self, message_id: int):
        c = self.conn.cursor()
        c.execute("DELETE FROM timers WHERE message_id=?", (message_id,))
        self.conn.commit()
        c.close()

    async def timer_callback(self, timer_data: TimerData):
        channel = self.bot.get_channel(timer_data.channel_id)
        if channel:
            notification_msg = await channel.fetch_message(timer_data.message_id)
            users_to_notify = []

            for reaction in notification_msg.reactions:
                if reaction.emoji == '⏰':
                    async for user in reaction.users():
                        if user.id != self.bot.user.id:
                            users_to_notify.append(user.mention)

            if users_to_notify:
                message = Timer.remove_role_mentions(timer_data.message)
                await channel.send(f"**{message}** \n{' '.join(users_to_notify)}")

            self.delete_timer(timer_data.message_id)

    @app_commands.command(
        name=CommandName.TIMER,
        description="Sets a notification timer. React with ⏰ to be notified when the time is up."
    )
    async def timer(
            self,
            interaction: discord.Interaction,
            message: str,
            hours: int,
            minutes: int,
    ):
        await interaction.response.send_message("Timer set!", ephemeral=True)

        sleep_time = Timer.convert_to_seconds(hours, minutes)
        unix_time = int(time.time()) + sleep_time

        notification_msg = await interaction.channel.send(
            f"**{message}** <t:{unix_time}:R>\nReact with ⏰ to get notified!"
        )

        await notification_msg.add_reaction('⏰')
        run_date = datetime.datetime.now() + datetime.timedelta(seconds=sleep_time)
        
        trigger = DateTrigger(run_date=run_date)
        timer_data = TimerData(
            message_id=notification_msg.id,
            channel_id=interaction.channel.id,
            user_id=interaction.user.id,
            message=message,
            run_date=run_date
        )
        self.scheduler.add_job(self.timer_callback, trigger, args=[timer_data])

        c = self.conn.cursor()
        c.execute("INSERT INTO timers (message_id, channel_id, user_id, message, run_date) VALUES (?, ?, ?, ?, ?)",
                  timer_data.to_row())
        self.conn.commit()
        c.close()

    @staticmethod
    def convert_to_seconds(hours: int = 0, minutes: int = 0, seconds: int = 0) -> int:
        return hours * 3600 + minutes * 60 + seconds

    @staticmethod
    def remove_role_mentions(message: str) -> str:
        words = message.split()
        filtered_words = [word for word in words if not word.startswith('<@')]
        return ' '.join(filtered_words)


async def setup(bot: commands.Bot):
    await bot.add_cog(Timer(bot))
