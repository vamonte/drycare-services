import time

from models.wrappers.mongo.base import Base
from bson.objectid import ObjectId
from models.wrappers.contracts import ConsuptionContract


class MongoConsuption(Base, ConsuptionContract):

    COLLECTION_NAME = "patients"

    @property
    def collection(self):
        return self.db[self.COLLECTION_NAME]

    def queries(self, pid, limit, offset, startdatetime, enddatetime):
        selectors = {"$and": [self._generate_id_selectors(pid),
                              {"consuptions.date": {"$gte": startdatetime,
                                                    "$lt": enddatetime}}]}
        return self._get(selectors, limit, offset)

    def save(self, pid, quantity, device):
        consuption = self.jsonify(quantity, device)
        return self.collection.update(self._generate_id_selectors(pid),
                                      {'$push': {"consuptions": consuption}})
        return alert

    def _get(self, selectors, limit, offset):
        datas = self.collection.aggregate([{"$unwind": "$consuptions"},
                                           {"$match": selectors},
                                           {"$project": {"consuptions": 1,
                                                         "_id": 0}},
                                           {"$skip": offset},
                                           {"$limit": limit}
                                           ])
        return self._format_result(datas['result'])

    def _format_result(self, result):
        alerts = list()
        for obj in result:
            datetime = obj["consuptions"]["date"]
            obj["consuptions"]["date"] = time.mktime(datetime.timetuple())
            alerts.append(obj["consuptions"])
        return alerts

    def _generate_id_selectors(self, pid):
        if len(pid) < 24:
            selector = {"bracelet": pid}
        else:
            selector = {"_id": ObjectId(pid)}
        return selector