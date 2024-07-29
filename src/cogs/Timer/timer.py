from __future__ import annotations

import os
import sqlite3
import asyncio
import time
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
import datetime
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
        for row in c.fetchall():
            message_id, channel_id, user_id, message, run_date = row
            print(f"Loading timer: {message_id}, {channel_id}, {user_id}, {message}, {run_date}")
            run_date = datetime.datetime.strptime(run_date, "%Y-%m-%d %H:%M:%S")
            if run_date > datetime.datetime.now():
                trigger = DateTrigger(run_date=run_date)
                print(f"Scheduling timer: {message_id}, {channel_id}, {user_id}, {message}, {run_date}")
                self.scheduler.add_job(self.notify_callback, trigger, args=[message_id, channel_id, user_id, message])

            else:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    print(f"Expired timer detected: {message_id}, {channel.name}")
                    self.bot.loop.create_task(channel.send(f"Sorry <@{user_id}>, the timer: **{message}** has expired "
                                                           f"while the bot was down."))
                    c.execute("DELETE FROM timers WHERE message_id=?", (message_id,))
                    self.conn.commit()
        c.close()

    async def notify_callback(self, message_id, channel_id, user_id, message):
        print(f"Notifying users for message ID {message_id} in channel ID {channel_id}")
        channel = self.bot.get_channel(channel_id)
        if channel:
            notification_msg = await channel.fetch_message(message_id)
            users_to_notify = []

            for reaction in notification_msg.reactions:
                if reaction.emoji == '⏰':
                    async for user in reaction.users():
                        if user.id != self.bot.user.id:
                            users_to_notify.append(user.mention)

            if users_to_notify:
                message = self.remove_role_mentions(message)
                await channel.send(f"**{message}** \n{' '.join(users_to_notify)}")

            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("DELETE FROM timers WHERE message_id=?", (message_id,))
            conn.commit()
            conn.close()

    @app_commands.command(
        name=CommandName.TIMER,
        description="Sets a timer for a specified duration and notifies you with a message when the time is up."
    )
    async def timer(
            self,
            interaction: discord.Interaction,
            message: str,
            hours: int,
            minutes: int,
    ):

        sleep_time = self.convert_to_seconds(hours, minutes)
        await interaction.response.send_message(f"Timer set for {hours} hours and {minutes} minutes.", ephemeral=True)
        await asyncio.sleep(sleep_time)
        await interaction.followup.send(f"{interaction.user.mention}, {message}", ephemeral=True)

    @app_commands.command(
        name=CommandName.NOTIFY,
        description="Sets a notification timer. React with ⏰ to be notified when the time is up."
    )
    async def notify(
            self,
            interaction: discord.Interaction,
            message: str,
            hours: int,
            minutes: int,
    ):
        await interaction.response.send_message("Timer set!", ephemeral=True)

        sleep_time = self.convert_to_seconds(hours, minutes)
        unix_time = int(time.time()) + sleep_time

        notification_msg = await interaction.channel.send(
            f"**{message}** <t:{unix_time}:R>\nReact with ⏰ to get notified!"
        )

        await notification_msg.add_reaction('⏰')
        run_date = datetime.datetime.now() + datetime.timedelta(seconds=sleep_time)
        print(f"Setting timer: {notification_msg.id}, {interaction.channel.id}, {interaction.user.id}, {message}, {run_date}")
        trigger = DateTrigger(run_date=run_date)
        self.scheduler.add_job(self.notify_callback, trigger, args=[notification_msg.id, interaction.channel.id, interaction.user.id, message])

        c = self.conn.cursor()
        c.execute("INSERT INTO timers (message_id, channel_id, user_id, message, run_date) VALUES (?, ?, ?, ?, ?)",
                  (notification_msg.id, interaction.channel.id, interaction.user.id, message, run_date.strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()

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
