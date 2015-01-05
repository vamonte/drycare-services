from models.base import Base


class Device(Base):

    MAX_LIMIT = 40
    NAME = "device"

    def __init__(self, name, location, ns, patient, *args, **kwargs):
        super(Device, self).__init__(*args, **kwargs)
        self.name = name
        self.location = location
        self.ns = ns
        self.patient_firstname = patient.get('firstname')
        self.patient_lastname = patient.get('lastname')
        self.patient_age = patient.get('age')

    @classmethod
    def get_last_devices(cls, limit):
        limit = int(limit) if int(limit) < cls.MAX_LIMIT else cls.MAX_LIMIT
        return cls.wrapper().get_last_devices(limit)

    @classmethod
    def save_device(cls, name, location, ns, patient_firstname,
                    patient_lastname, patient_age):
        return cls.wrapper().save_device(name, location, ns,
                                         patient_firstname,
                                         patient_lastname, patient_age)

    @classmethod
    def get_device(cls, _id):
        return cls.wrapper().get_device(_id)

    @classmethod
    def remove_device(cls, _id):
        return cls.wrapper().remove_device(_id)
