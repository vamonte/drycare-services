from flask.ext.restful import Resource, reqparse
from flask import Response

from bson.json_util import dumps


class BaseService(Resource):

    def _build_response(self, msg, status):
        return Response(msg, status=status, mimetype='application/json')

    def build_success_response(self, msg):
        return self._build_response(dumps(msg), 200)

    def build_error_response(self, msg):
        return self._build_response(dumps(msg), 404)
