from models.base import Base
from datetime import datetime


class Alert(Base):

    NAME = "alert"

    def __init__(self, *args, **kwargs):
        super(Alert, self).__init__(*args, **kwargs)

    @classmethod
    def all(cls, limit, offset):
        return cls.wrapper().all(limit, offset)

    @classmethod
    def queries(cls, pid, limit, offset, date):
        startdatetime = datetime(year=2015, month=01, day=01)
        enddatetime = datetime(year=3015, month=01, day=01)
        if date:
            startdatetime = date
            enddatetime = datetime(year=date.year,
                                   month=date.month,
                                   day=date.day+1)

        return cls.wrapper().queries(pid, limit, offset, startdatetime,
                                     enddatetime)

    @classmethod
    def save(cls, pid, queue, level, device):
        return cls.wrapper().save(pid, queue, level, device)