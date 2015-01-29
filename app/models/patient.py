from models.base import Base


class Patient(Base):

    NAME = "patient"

    def __init__(self):
        super(Patient, self).__init__(*args, **kwargs)

    @classmethod
    def save(cls, bracelet, firstname, lastname, age, weight, **kwargs):
        min_consuption_day = cls.calculate_min_consuption_day(weight)
        return cls.wrapper().save(bracelet, firstname, lastname, age, weight,
                                  min_consuption_day)

    @classmethod
    def queries(cls, limit, offset, filters):
        return cls.wrapper().queries(limit, offset, filters)

    @classmethod
    def get(cls, pid):
        return cls.wrapper().get(pid)

    @staticmethod
    def calculate_min_consuption_day(weight):
        return float((((int(weight)-20)*15)+500))/1000

    @classmethod
    def update(cls, pid, firstname=None, lastname=None, age=None,
               weight=None, bracelet=None, **kwargs):
        if weight:
            min_consuption_day = cls.calculate_min_consuption_day(weight)
        else:
            min_consuption_day = None
        return cls.wrapper().update(pid, firstname=firstname,
                                    lastname=lastname, age=age, weight=weight,
                                    min_consuption_day=min_consuption_day,
                                    bracelet=bracelet)

    @classmethod
    def get_min_consuption(cls, pid):
        min_consuption = cls.wrapper().get(pid)[0]["min_consuption_day"]
        ten = (1.5/6.5) * min_consuption
        fourteen = ten + ((2/6.5) * min_consuption)
        sixteen = fourteen + ((2/6.5) * min_consuption)
        twenty = sixteen + ((1/6.5) * min_consuption)

        return {"10": ten, "14": fourteen, "16": sixteen, "20": twenty}
