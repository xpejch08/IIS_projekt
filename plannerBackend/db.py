from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.Integer)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'role': self.role,
        }


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    shortcut = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    annotation = db.Column(db.Text)
    credits = db.Column(db.Integer)
    id_guarantor = db.Column(db.Integer, db.ForeignKey('users.id'))

    guarantor = db.relationship('User')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

