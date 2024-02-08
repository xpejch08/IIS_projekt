from flask import Flask
from flask_session import Session

from db import db
from routes import my_routes
from flask_cors import CORS
from flasgger import Swagger
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    swagger = Swagger(app)
    ##secret key
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SECRET_KEY"] = "MYSECRETKEY"

    Session(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = (
    )
  # MySQL database
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(my_routes)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
