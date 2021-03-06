from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import os

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


def create_app(test: bool):
    app = Flask(__name__)
    app.config['TESTING'] = test
    app.config['FLASK_APP'] = 'app/app.py'
    app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
    app.secret_key = 'eminem'

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_2', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True

    jwt = JWT(app=app, authentication_handler=authenticate, identity_handler=identity) # /auth
    api = Api(app)
    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(StoreList, '/stores')
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(UserRegister, '/register')
    return app


app = create_app(False)


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)