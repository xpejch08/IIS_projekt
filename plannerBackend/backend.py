from flask import Flask
from db import db
from routes import my_routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/iisdatabase'
  # MySQL database
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(my_routes)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
