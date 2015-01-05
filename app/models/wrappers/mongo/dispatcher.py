from models.wrappers.mongo.device import MongoDevice
from models.wrappers.mongo.user import MongoUser


class MongoDispatcher(object):

    WRAPPERS = {'device': MongoDevice,
                'user': MongoUser}

    @classmethod
    def get(cls, name):
        return cls.WRAPPERS.get(name)