from flask.ext.restful import reqparse

from models.patient import Patient as Pmodel

from services.base import BaseService
from services.user import auth


class Patients(BaseService):

    def __init__(self, *args, **kwargs):
        self.post_parser = self._build_post_parser()
        self.get_parser = self._build_get_parser()
        super(Patients, self).__init__(*args, **kwargs)

    @auth.login_required
    def post(self):
        kwargs = self.post_parser.parse_args()
        patient = Pmodel.save(**kwargs)
        return patient

    @auth.login_required
    def get(self):
        kwargs = self.get_parser.parse_args()
        limit = kwargs["limit"] if kwargs["limit"] else 50
        offset = kwargs["offset"] if kwargs["offset"] else 0
        filters = kwargs['filters'] if kwargs["filters"] else ""
        return self.build_success_response(Pmodel.queries(limit, offset,
                                                          filters))

    def _build_post_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstname', type=str, required=True,
                            help="{'firstname':'Value required'}",
                            location='json')
        parser.add_argument('lastname', type=str, required=True,
                            help="{'lastname':'Value required'}",
                            location='json')
        parser.add_argument('age', type=str, required=True,
                            help="{'age': 'Value required'}",
                            location='json')
        parser.add_argument('weight', type=str, required=True,
                            help="{'weight': 'Value required'}",
                            location='json')
        parser.add_argument('bracelet', type=str, required=True,
                            help="{'bracelet': 'Value required'}",
                            location='json')
        return parser

    def _build_get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, location='args')
        parser.add_argument('offset', type=int, location='args')
        parser.add_argument('filters', type=str, location='args')
        return parser


class Patient(BaseService):

    def __init__(self, *args, **kwargs):
        self.put_parser = self._build_put_parser()
        super(Patient, self).__init__(*args, **kwargs)

    @auth.login_required
    def get(self, pid):
        return self.build_success_response(Pmodel.get(pid))

    @auth.login_required
    def put(self, pid):
        kwargs = self.put_parser.parse_args()
        if not(kwargs.get('firstname') or kwargs.get('lastname')
               or kwargs.get('age') or kwargs.get('weight')
               or kwargs.get('bracelet')):
            abort(404)
        return self.build_success_response(Pmodel.update(pid, **kwargs))

    def _build_put_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstname', type=str,
                            help="{'firstname':'Value required'}",
                            location='json')
        parser.add_argument('lastname', type=str,
                            help="{'lastname':'Value required'}",
                            location='json')
        parser.add_argument('age', type=str,
                            help="{'age': 'Value required'}",
                            location='json')
        parser.add_argument('weight', type=str,
                            help="{'weight': 'Value required'}",
                            location='json')
        parser.add_argument('bracelet', type=str,
                            help="{'bracelet': 'Value required'}",
                            location='json')
        return parser
