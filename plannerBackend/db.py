from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'role': self.role,
        }
