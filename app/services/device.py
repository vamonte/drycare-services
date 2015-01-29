#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.restful import reqparse
from flask import Response, abort

from models.device import Device as Dmodel

from services.user import auth
from services.base import BaseService


class Devices(BaseService):

    def __init__(self, *args, **kwargs):
        self.post_parser = self._build_post_parser()
        self.get_parser = self._build_get_parser()
        super(Devices, self).__init__(*args, **kwargs)

    @auth.login_required
    def get(self):
        kwargs = self.get_parser.parse_args()
        limit = kwargs["limit"] if kwargs["limit"] else 10
        offset = kwargs['offset'] if kwargs['offset'] else 0
        filters = kwargs['filters'] if kwargs["filters"] else ""
        return self.build_success_response(Dmodel.queries(limit, offset,
                                                          filters))

    @auth.login_required
    def post(self):
        kwargs = self.post_parser.parse_args()
        return self.build_success_response(Dmodel.save(**kwargs))

    def _build_post_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('did', type=str, required=True,
                            help="{'did': 'Value required'}",
                            location='json')
        parser.add_argument('name', type=unicode, required=True,
                            help="{'name':'Value required'}", location='json')
        parser.add_argument('location', type=unicode, required=True,
                            help="{'location':'Value required'}",
                            location='json')
        return parser

    def _build_get_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, location='args')
        parser.add_argument('offset', type=int, location='args')
        parser.add_argument('filters', type=str, location='args')
        return parser


class Device(BaseService):

    def __init__(self, *args, **kwargs):
        self.put_parser = self._build_put_parser()
        super(Device, self).__init__(*args, **kwargs)

    @auth.login_required
    def get(self, did):
        device = Dmodel.get(did)
        if len(device) == 0:
            abort(404)
        return self.build_success_response(device)

    @auth.login_required
    def delete(self, did):
        result = Dmodel.remove(did)
        if result["n"] == 0:
            abort(404)
        return self.build_success_response({"status": 200,
                                            "message": "Device removed"})

    @auth.login_required
    def put(self, did):
        _id = did
        kwargs = self.put_parser.parse_args()
        if not(kwargs.get('name') or kwargs.get('location')):
            abort(404)
        return self.build_success_response(Dmodel.update(_id=_id, **kwargs))

    def _build_put_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('did', type=str,
                            location='json')
        parser.add_argument('name', type=str,
                            location='json')
        parser.add_argument('location', type=str,
                            location='json')
        return parser
