from flask.ext.restful import reqparse
from flask.ext.restful import inputs

from models.consuption import Consuption as Cmodel
from models.patient import Patient as Pmodel

from services.base import BaseService
from services.user import auth


class Consuptions(BaseService):

    def __init__(self, *args, **kwargs):
        self.post_parser = self._build_post_parser()
        self.get_parser = self._build_get_parser()
        super(Consuptions, self).__init__(*args, **kwargs)

    @auth.login_required
    def get(self, pid):
        kwargs = self.get_parser.parse_args()
        start_date = kwargs["start_date"]
        end_date = kwargs["end_date"]
        limit = kwargs["limit"] if kwargs['limit'] else 500
        offset = kwargs["offset"] if kwargs["offset"] else 0
        return self.build_success_response(Cmodel.queries(pid, limit, offset,
                                                          start_date, end_date))

    @auth.login_required
    def post(self, pid):
        kwargs = self.post_parser.parse_args()
        Cmodel.save(pid, **kwargs)
        return self.build_success_response({"status": 200,
                                            "message": "Consuption added"})

    def _build_post_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('quantity', type=float, required=True,
                            help="{'quantity': 'Value required'}",
                            location='json')
        parser.add_argument('device', type=str, required=True,
                            help="{'device':'Value required'}",
                            location='json')
        return parser

    def _build_get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_date', type=inputs.date, location='args', required=False)
        parser.add_argument('end_date', type=inputs.date, location='args', required=False)
        parser.add_argument('limit', type=int, location='args', required=False)
        parser.add_argument('offset', type=int, location='args', required=False)
        return parser


class MinConsuptions(BaseService):

    def get(self, pid):
        return self.build_success_response(Pmodel.get_min_consuption(pid))
