from models.wrappers.mongo.base import Base
from models.wrappers.contracts import PatientContract
from bson.objectid import ObjectId


class MongoPatient(Base, PatientContract):

    COLLECTION_NAME = "patients"
    URI = "/api/patients/{pid}"
    BRACELET_FORMAT = "bracelet"

    @property
    def collection(self):
        return self.db[self.COLLECTION_NAME]

    def save(self, bracelet, firstname, lastname, age, weight,
             min_consuption_day):
        patient = self.jsonify(bracelet, firstname, lastname, age, weight,
                               min_consuption_day, [], [])
        pid = self.collection.save(patient)
        return {'uri': self.URI.format(pid=pid)}

    def _get(self, selectors, limit, offset):
        datas = self.collection.aggregate([{'$match': selectors},
                                           {'$sort': {'_id': -1}},
                                           {'$project': {'_id': 1,
                                                         'name': 1,
                                                         'firstname': 1,
                                                         'lastname': 1,
                                                         'age': 1,
                                                         'weight': 1,
                                                         'min_consuption_day': 1,
                                                         'bracelet': 1,
                                                         'uri': {'$literal': self.URI}
                                                         }},
                                           {'$skip': offset},
                                           {'$limit': limit},
                                           ])
        return self._format_result(datas['result'])

    def queries(self, limit, offset, filters):
        selectors = {"$or": [{'firstname': {"$regex": filters,
                                            "$options": "-i"}},
                             {'lastname': {"$regex": filters,
                                           "$options": "-i"}},
                             {'name': {"$regex": filters,
                                       "$options": "-i"}},
                             {'bracelet': {"$regex": filters,
                                           "$options": "-i"}}
                             ]}
        return self._get(selectors, limit, offset)

    def get(self, pid):
        selectors = self._generate_id_selectors(pid)
        return self._get(selectors, 1, 0)

    def update(self, pid, **kwargs):
        updated_values = {key: value for (key, value) in kwargs.items() if value is not None}
        if kwargs.get("lastname") and kwargs.get("firstname"):
            updated_values["name"] = "{f} {l}".format(f=kwargs['firstname'],
                                                      l=kwargs['lastname'])
        patient = self.collection.find_and_modify(self._generate_id_selectors(pid),
                                                  {"$set": updated_values},
                                                  new=True)
        patient['uri'] = self.URI
        del patient['consumptions']
        del patient['alerts']
        return self._format_result([patient], is_list=False)

    def _generate_id_selectors(self, pid):
        if len(pid) < 24:
            selector = {"bracelet": pid}
        else:
            selector = {"_id": ObjectId(pid)}
        return selector

    def _format_result(self, aggregate_result, is_list=True):
        patients = list()
        for obj in aggregate_result:
            obj['uri'] = obj['uri'].format(pid=str(obj["_id"]))
            patients.append(obj)
        if not is_list:
            return patients[0]
        return patients
        