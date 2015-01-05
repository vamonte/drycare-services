from flask.ext.restful import reqparse
from flask import Response, abort

from models.device import Device as Dmodel

from services.user import auth
from services.base import BaseService


class DeviceList(BaseService):

    def __init__(self, *args, **kwargs):
        self.post_parser = self._build_post_parser()
        self.get_parser = self._build_get_parser()
        super(DeviceList, self).__init__(*args, **kwargs)

    @auth.login_required
    def get(self):
        kwargs = self.get_parser.parse_args()
        limit = kwargs["limit"] if kwargs["limit"] else 10
        return self.build_success_response(Dmodel.get_last_devices(limit))

    @auth.login_required
    def post(self):
        kwargs = self.post_parser.parse_args()
        device = Dmodel.save_device(**kwargs)

    def _build_post_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="{'name':'Value required'}", location='json')
        parser.add_argument('location', type=str, required=True,
                            help="{'location':'Value required'}",
                            location='json')
        parser.add_argument('ns', type=str, required=True,
                            help="{'ns': 'Value required'}",
                            location='json')
        parser.add_argument('patient_firstname', type=str, required=True,
                            help="{'patient_firstname': 'Value required'}",
                            location='json')
        parser.add_argument('patient_lastname', type=str, required=True,
                            help="{'patient_lastname': 'Value required'}",
                            location='json')
        parser.add_argument('patient_age', type=str, required=True,
                            help="{'patient_age': 'Value required'}",
                            location='json')
        return parser

    def _build_get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, location='args')
        parser.add_argument('offset', type=int, location='args')
        return parser


class Device(BaseService):

    def __init__(self, *args, **kwargs):
        super(Device, self).__init__(*args, **kwargs)

    @auth.login_required
    def get(self, did):
        device = Dmodel.get_device(did)
        if len(device) == 0:
            abort(404)
        return self.build_success_response(device)

    @auth.login_required
    def delete(self, did):
        result = Dmodel.remove_device(did)
        if result["n"] == 0:
            abort(404)
        return self.build_success_response("Device removed")
