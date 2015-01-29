from flask.ext.restful import reqparse
from flask.ext.restful import inputs

from models.alert import Alert as Amodel

from services.base import BaseService, q
from services.user import auth


class AllAlerts(BaseService):

    def __init__(self, *args, **kwargs):
        self.get_parser = self._build_get_parser()
        super(AllAlerts, self).__init__(*args, **kwargs)

    def _build_get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, location='args', required=False)
        parser.add_argument('offset', type=int, location='args', required=False)
        return parser

    @auth.login_required
    def get(self):
        kwargs = self.get_parser.parse_args()
        limit = kwargs["limit"] if kwargs['limit'] else 50
        offset = kwargs["offset"] if kwargs["offset"] else 0
        return self.build_success_response(Amodel.all(limit, offset))


class Alerts(BaseService):

    def __init__(self, *args, **kwargs):
        self.post_parser = self._build_post_parser()
        self.get_parser = self._build_get_parser()
        super(Alerts, self).__init__(*args, **kwargs)

    @auth.login_required
    def get(self, pid):
        kwargs = self.get_parser.parse_args()
        date = kwargs["date"]
        limit = kwargs["limit"] if kwargs['limit'] else 50
        offset = kwargs["offset"] if kwargs["offset"] else 0
        return self.build_success_response(Amodel.queries(pid, limit, offset,
                                                          date))

    @auth.login_required
    def post(self, pid):
        kwargs = self.post_parser.parse_args()
        return self.build_success_response(Amodel.save(pid, q, **kwargs))

    def _build_post_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('level', type=str, required=True,
                            help="{'level': 'Value required'}",
                            location='json')
        parser.add_argument('device', type=str, required=True,
                            help="{'device':'Value required'}",
                            location='json')
        return parser

    def _build_get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=inputs.date, location='args', required=False)
        parser.add_argument('limit', type=int, location='args', required=False)
        parser.add_argument('offset', type=int, location='args', required=False)
        return parser