from models.wrappers.mongo.device import MongoDevice
from models.wrappers.mongo.user import MongoUser
from models.wrappers.mongo.patient import MongoPatient
from models.wrappers.mongo.alert import MongoAlert
from models.wrappers.mongo.consuption import MongoConsuption


class MongoDispatcher(object):

    WRAPPERS = {'device': MongoDevice,
                'user': MongoUser,
                'patient': MongoPatient,
                'alert': MongoAlert,
                'consuption': MongoConsuption}

    @classmethod
    def get(cls, name):
        return cls.WRAPPERS.get(name)