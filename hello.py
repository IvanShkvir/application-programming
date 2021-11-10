from flask import Flask
from waitress import serve
from flask_bcrypt import Bcrypt
from app import api_blueprint

api = Flask(__name__)
api.register_blueprint(api_blueprint)
bcrypt = Bcrypt(api)


if __name__ == "__main__":
    serve(api, port=5000)