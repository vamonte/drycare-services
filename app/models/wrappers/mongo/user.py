from models.wrappers.contracts import UserContract
from models.wrappers.mongo.base import Base

from bson.objectid import ObjectId


class MongoUser(Base, UserContract):

    COLLECTION_NAME = "user"

    @property
    def collection(self):
        return self.db[self.COLLECTION_NAME]

    def save(self, name, password, mail):
        user = self.jsonify(name, password, mail)
        return self.collection.save(user)

    def get_by_id(self, uid):
        return list(self.collection.find({'_id': ObjectId(uid)}))

    def get_by_name(self, name):
        return list(self.collection.find({'name': name}))