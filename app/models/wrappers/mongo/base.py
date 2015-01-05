import os
import pymongo
from abc import ABCMeta


class Base(object):
    __metaclass__ = ABCMeta

    HOST = os.environ["DB_PORT_27017_TCP_ADDR"]
    PORT = int(os.environ['DB_PORT_27017_TCP_PORT'])
    NAME = "drycare"

    @property
    def db(self):
        try:
            conn = pymongo.Connection(host=self.HOST, port=self.PORT)
        except KeyError:
            raise Exception("You have to link your web container with"
                            " a mongo container")
        return conn[self.NAME]
