
from abc import ABCMeta, abstractmethod
from bson.objectid import ObjectId
from datetime import datetime


class ModellingContract(object):

    @staticmethod
    def device_jsonify(did, name, location):
        return {'_id': ObjectId(),
                'did': did,
                'name': name,
                'location': location,
                }

    @staticmethod
    def patient_jsonify(bracelet, firstname, lastname, age, weight,
                        min_consuption_day, consuption, alert):
        return {'_id': ObjectId(),
                'bracelet': bracelet,
                'firstname': firstname,
                'lastname': lastname,
                'age': age,
                'weight': weight,
                'min_consuption_day': min_consuption_day,
                'consumptions': consuption,
                'alerts': alert,
                'name': "{f} {l}".format(f=firstname,
                                         l=lastname)
                }

    @staticmethod
    def alert_jsonify(level, device):
        return {'_id': ObjectId(),
                'date': datetime.utcnow(),
                'level': level,
                'device': ObjectId(device)
                }

    @staticmethod
    def consuption_jsonify(quantity, device):
        return {'_id': ObjectId(),
                'date': datetime.utcnow(),
                'quantity': quantity,
                'device': ObjectId(device)
                }


class DeviceContract(object):
    __metaclass__ = ABCMeta

    def jsonify(self, did, name, location):
        return ModellingContract.device_jsonify(did, name, location)


class PatientContract(object):
    __metaclass__ = ABCMeta

    def jsonify(self, bracelet, firstname, lastname, age, weight,
                min_consuption_day, consuption, alert):
        return ModellingContract.patient_jsonify(bracelet, firstname, lastname,
                                                 age, weight,
                                                 min_consuption_day,
                                                 consuption, alert)


class AlertContract(object):
    __metaclass__ = ABCMeta

    def jsonify(self, level, device):
        return ModellingContract.alert_jsonify(level, device)


class ConsuptionContract(object):
    __metaclass__ = ABCMeta

    def jsonify(self, quantity, device):
        return ModellingContract.consuption_jsonify(quantity, device)


class UserContract(object):

    @abstractmethod
    def save(self, name, password, mail):
        pass

    def jsonify(self, name, password, mail):
        return {'name': name,
                'password': password,
                'mail': mail
                }
