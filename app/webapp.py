import os

from flask import Flask
from flask.ext.restful import Api

from services.device import DeviceList, Device
from services.user import UserList
from services.token import Token

app = Flask(__name__)
api = Api(app)


@app.route("/")
def index():
    return str(os.environ)


api.add_resource(DeviceList, '/api/devices')
api.add_resource(Device, '/api/devices/<string:did>')
api.add_resource(UserList, '/api/users')
api.add_resource(Token, '/api/token')


if __name__ == "__main__":
    app.run()
