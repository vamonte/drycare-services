from models.base import Base
from datetime import datetime


class Consuption(Base):

    NAME = "consuption"

    def __init__(self, *args, **kwargs):
        super(Consuption, self).__init__(*args, **kwargs)

    @classmethod
    def queries(cls, pid, limit, offset, start_date, end_date):
        
        if start_date:
            startdatetime = start_date
            if not end_date:
                enddatetime = datetime(year=start_date.year,
                                       month=start_date.month,
                                       day=start_date.day+1)
            else:
                enddatetime = end_date
        else:
            startdatetime = datetime(year=2015, month=01, day=01)
            enddatetime = datetime(year=3015, month=01, day=01)
        return cls.wrapper().queries(pid, limit, offset, startdatetime,
                                     enddatetime)

    @classmethod
    def save(cls, pid, quantity, device):
        return cls.wrapper().save(pid, quantity, device)