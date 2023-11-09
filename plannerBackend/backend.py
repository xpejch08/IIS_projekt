from flask import Flask
from db import db
from routes import my_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "mysql+pymysql://avnadmin:AVNS_OsQ-AxAVvd-8vaWLLHy@"
        "mysql-iis-xpejch08-pejcharstepan-iis.a.aivencloud.com:10064/"
        "defaultdb?ssl_ca=ca.pem"
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
