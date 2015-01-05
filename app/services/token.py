from flask.ext.restful import Resource, reqparse
from flask import g

from services.base import BaseService
from services.user import auth


class Token(BaseService):

    def __init__(self, *args, **kwargs):
        super(Token, self).__init__(*args, **kwargs)

    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return self.build_success_response({'token': token.decode("ascii")})
