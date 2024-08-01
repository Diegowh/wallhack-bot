from __future__ import annotations

import datetime as dt
from pydantic import BaseModel


class TimerData(BaseModel):
    message_id:int
    channel_id: int
    user_id: int
    message: str
    run_date: dt.datetime

    @classmethod
    def from_row(cls, row) -> TimerData:
        message_id, channel_id, user_id, message, run_date = row
        run_date = dt.datetime.strptime(run_date, "%Y-%m-%d %H:%M:%S")
        return cls(
            message_id=message_id,
            channel_id=channel_id,
            user_id=user_id,
            message=message,
            run_date=run_date
        )

    def to_row(self):
        return(
            self.message_id,
            self.channel_id,
            self.user_id,
            self.message,
            self.run_date.strftime("%Y-%m-%d %H:%M:%S")
        )