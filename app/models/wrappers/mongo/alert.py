import time

from services.base import q
from models.wrappers.mongo.base import Base
from bson.objectid import ObjectId
from models.wrappers.contracts import AlertContract


class MongoAlert(Base, AlertContract):

    COLLECTION_NAME = "patients"

    @property
    def collection(self):
        return self.db[self.COLLECTION_NAME]

    def all(self, limit, offset):
        project = {"alerts": 1, "name": 1, "_id": 0}
        return self._get({}, project, limit, offset)

    def queries(self, pid, limit, offset, startdatetime, enddatetime):
        selectors = {"$and": [self._generate_id_selectors(pid),
                              {"alerts.date": {"$gte": startdatetime,
                                               "$lt": enddatetime}}]}
        project = {"alerts": 1, "_id": 0}
        return self._get(selectors, project, limit, offset)

    def save(self, pid, queue, level, device):
        alert = self.jsonify(level, device)
        q.put({"type": "alert", "object": alert})
        return self.collection.update(self._generate_id_selectors(pid),
                                      {'$push': {"alerts": alert}})

    def _get(self, selectors, project, limit, offset):
        datas = self.collection.aggregate([{"$unwind": "$alerts"},
                                           {"$match": selectors},
                                           {"$project": project},
                                           {"$sort": {'alerts._id': -1}},
                                           {"$skip": offset},
                                           {"$limit": limit}
                                           ])
        return self._format_result(datas['result'])

    def _format_result(self, result):
        alerts = list()
        for obj in result:
            datetime = obj["alerts"]["date"]
            obj["alerts"]["date"] = time.mktime(datetime.timetuple())
            alerts.append(obj)
        return alerts

    def _generate_id_selectors(self, pid):
        if len(pid) < 24:
            selector = {"bracelet": pid}
        else:
            selector = {"_id": ObjectId(pid)}
        return selector