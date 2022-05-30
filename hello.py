from datetime import timedelta

from flask import Flask
# from waitress import serve
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app import api_blueprint, s, TokenBlockList

ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.register_blueprint(api_blueprint)
bcrypt = Bcrypt(app)

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = s.query(TokenBlockList.id).filter_by(jti=jti).first()
    return token is not None


if __name__ == "__main__":
    app.run(debug=True)
    # serve(app, port=5000)
