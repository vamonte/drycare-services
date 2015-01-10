from models.base import Base
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (BadSignature, SignatureExpired,
                          TimedJSONWebSignatureSerializer as Serializer)
from bson.json_util import dumps, loads


class User(Base):

    NAME = "user"
    SECRET_KEY = "The secret salt to the authentication will be never find."

    def __init__(self, _id, name, password, mail, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.id = _id
        self.name = name
        self.password = password
        self.mail = mail

    @staticmethod
    def hash_password(password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(self.SECRET_KEY, expires_in=expiration)
        return s.dumps(dumps(self.id))

    @classmethod
    def save(cls, name, password, mail):
        passw = cls.hash_password(password)
        return cls.wrapper().save(name, passw, mail)

    @classmethod
    def get_by_id(cls, uid):
        users = cls.wrapper().get_by_id(uid)
        if len(users) == 0:
            return None
        return users[0]

    @classmethod
    def get_by_name(cls, name):
        users = cls.wrapper().get_by_name(name)
        if len(users) == 0:
            return None
        return User(**users[0])

    @classmethod
    def verify_auth_token(cls, token):
        s = Serializer(cls.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        _id = loads(data)
        return User(**cls.get_by_id(str(_id)))
