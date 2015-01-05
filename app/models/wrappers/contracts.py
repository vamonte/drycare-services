from abc import ABCMeta, abstractmethod


class DeviceContract(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_last_devices(self, limit):
        pass

    @abstractmethod
    def get_device(self, _id):
        pass

    @abstractmethod
    def save_device(self, name, location, ns, patient_firstname,
                    patient_lastname, patient_age):
        pass

    @abstractmethod
    def remove_device(self, _id):
        pass

    def jsonify(self, name, location, ns, patient_firstname,
                patient_lastname, patient_age):
        return {'name': name,
                'location': location,
                'ns': ns,
                'patient': {'firstname': patient_firstname,
                            'lastname': patient_lastname,
                            'age': patient_age
                            }}


class UserContract(object):

    @abstractmethod
    def save(self, name, password, mail):
        pass

    def jsonify(self, name, password, mail):
        return {'name': name,
                'password': password,
                'mail': mail}