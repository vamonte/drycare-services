#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask.ext.restful import Api
from flask.ext.restful.representations.json import output_json
output_json.func_globals['settings'] = {'ensure_ascii': False, 'encoding': 'utf8'}

from services.device import Devices, Device
from services.user import UserList
from services.token import Token

from services.patient import Patients, Patient
from services.alert import Alerts
from services.consuption import Consuptions, MinConsuptions


app = Flask(__name__)
api = Api(app)


@app.route("/")
def index():
    return str(os.environ)


api.add_resource(Devices, '/api/devices')
api.add_resource(Device, '/api/devices/<string:did>')
api.add_resource(Patients, '/api/patients')
api.add_resource(Patient, '/api/patients/<string:pid>')
api.add_resource(Alerts, '/api/patients/<string:pid>/alerts')
api.add_resource(Consuptions, '/api/patients/<string:pid>/consuptions')
api.add_resource(MinConsuptions, '/api/patients/<string:pid>/min_consuptions')
api.add_resource(UserList, '/api/users')
api.add_resource(Token, '/api/token')


if __name__ == "__main__":
    app.run()
