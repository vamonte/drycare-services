from flask.ext.restful import reqparse
from flask.ext.httpauth import HTTPBasicAuth

from flask import g

from models.user import User as Umodel

from services.base import BaseService

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    user = Umodel.verify_auth_token(username_or_token)
    if not user:
        user = Umodel.get_by_name(username_or_token)
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


class UserList(BaseService):

    def __init__(self, *args, **kwargs):
        self.post_parser = self._build_post_parser()
        super(UserList, self).__init__(*args, **kwargs)

    def post(self):
        kwargs = self.post_parser.parse_args()
        user = Umodel.save(**kwargs)

    def _build_post_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="{'name': 'Value required'}",
                            location="json")
        parser.add_argument('password', type=str, required=True,
                            help="{'password': 'Value required'}",
                            location="json")
        parser.add_argument('mail', type=str, required=True,
                            help="{'mail': 'Value required'}",
                            location="json")
        return parser
