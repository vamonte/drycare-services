from models.base import Base
from datetime import datetime


class Consuption(Base):

    NAME = "consuption"

    def __init__(self, *args, **kwargs):
        super(Consuption, self).__init__(*args, **kwargs)

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
    def save(cls, pid, quantity, device):
        return cls.wrapper().save(pid, quantity, device)