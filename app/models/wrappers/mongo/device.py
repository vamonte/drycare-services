from models.wrappers.contracts import DeviceContract
from models.wrappers.mongo.base import Base
from bson.objectid import ObjectId


class MongoDevice(Base, DeviceContract):

    COLLECTION_NAME = "devices"

    @property
    def collection(self):
        return self.db[self.COLLECTION_NAME]

    def _get_devices(self, limit, selectors=None, sort=None):
        sort = sort or [['_id', -1]]
        limit = limit
        return self.collection.find(selectors).sort(sort).limit(limit)

    def get_last_devices(self, limit):
        return list(self._get_devices(limit=limit))

    def get_device(self, _id):
        return list(self._get_devices(limit=1, selectors={'_id': ObjectId(_id)}
                                      ))

    def save_device(self, name, location, ns, patient_firstname,
                    patient_lastname, patient_age):
        device = self.jsonify(name, location, ns,
                              patient_firstname, patient_lastname,
                              patient_age)
        return self.collection.save(device)

    def remove_device(self, _id):
        return self.collection.remove({'_id': ObjectId(_id)}, safe=True)
        