from models.wrappers.mongo.dispatcher import MongoDispatcher


class Base(object):

    WRAPPERS_DISPATCHER = {'MONGO': MongoDispatcher}
    WRAPPERS_DISPATCHER_NAME = 'MONGO'
    NAME = ''

    @classmethod
    def dispatcher(cls):
        return cls.WRAPPERS_DISPATCHER[cls.WRAPPERS_DISPATCHER_NAME]

    @classmethod
    def wrapper(cls):
        Wrapper = cls.dispatcher().get(cls.NAME)
        return Wrapper()
