#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.wrappers.contracts import DeviceContract
from models.wrappers.mongo.base import Base
from bson.objectid import ObjectId


class MongoDevice(Base, DeviceContract):

    COLLECTION_NAME = "devices"
    URI = "/api/devices/{did}"

    @property
    def collection(self):
        return self.db[self.COLLECTION_NAME]

    def queries(self, limit, offset, filters):
        selectors = {'$or': [{"location": {'$regex': filters,
                                           '$options': '-i'}},
                             {"name": {'$regex': filters,
                                       '$options': '-i'}}]}
        return self._get(selectors, limit, offset)

    def get(self, did):
        selectors = self._generate_id_selectors(did)
        return self._get(selectors, 1, 0)

    def save(self, name, location, did):
        device = self.jsonify(did, name, location)
        did = self.collection.save(device)
        return {'uri': self.URI.format(did=did)}

    def remove(self, did):
        return self.collection.remove({'_id': ObjectId(did)}, safe=True)

    def update(self, _id, **kwargs):
        updated_values = {key: value for (key, value) in kwargs.items() if value is not None}
        dev = self.collection.find_and_modify(self._generate_id_selectors(_id),
                                              {"$set": updated_values},
                                              new=True)
        dev['uri'] = self.URI
        return self._format_result([dev], is_list=False)

    def _get(self, selectors, limit, offset):
        datas = self.collection.aggregate([{'$match': selectors},
                                           {'$sort': {'_id': -1}},
                                           {'$project': {'_id': 1,
                                                         'did': 1,
                                                         'name': 1,
                                                         'location': 1,
                                                         'uri': {'$literal': self.URI}}},
                                           {'$skip': offset},
                                           {'$limit': limit}])
        return self._format_result(datas['result'])

    def _generate_id_selectors(self, did):
        if len(did) < 24:
            selector = {"did": did}
        else:
            selector = {"_id": ObjectId(did)}
        return selector

    def _format_result(self, result, is_list=True):
        devices = list()
        for obj in result:
            obj["uri"] = obj['uri'].format(did=obj["_id"])
            devices.append(obj)
        if not is_list:
            return devices[0]
        return devices