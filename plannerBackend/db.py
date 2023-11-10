from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
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
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    shortcut = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    annotation = db.Column(db.Text)
    credits = db.Column(db.Integer)
    guarantor_name = db.Column(db.String(255), db.ForeignKey('users.name'))

    guarantor = db.relationship('User')

    def as_dict(self):
        return {
            'id': self.id,
            'shortcut': self.shortcut,
            'name': self.name,
            'annotation': self.annotation,
            'credits': self.credits,
            'guarantor_name': self.guarantor_name,
        }



class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    capacity = db.Column(db.Integer)

    # Relationships
    schedules = db.relationship('Schedule', back_populates='room')

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'capacity': self.capacity
        }


class SubjectGuardians(db.Model):
    __tablename__ = 'subject_guardians'
    shortcut = db.Column(db.String(255), db.ForeignKey('subjects.shortcut', ondelete='CASCADE'), primary_key=True)
    teacher_name = db.Column(db.String(255), db.ForeignKey('users.name', ondelete='CASCADE'), primary_key=True)

    # Relationships
    subject = db.relationship('Subject', backref=db.backref('subject_guardians', cascade='all, delete'))
    teacher = db.relationship('User', backref=db.backref('subject_guardians', cascade='all, delete'))


class TeachingActivity(db.Model):
    __tablename__ = 'teaching_activities'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    label = db.Column(db.String(255))
    duration = db.Column(db.Integer)
    repetition = db.Column(db.String(255))
    subject_shortcut = db.Column(db.String(255), db.ForeignKey('subjects.shortcut'))

    # Relationships
    schedules = db.relationship('Schedule', back_populates='teaching_activity')
    subject = db.relationship('Subject')

    def as_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'duration': self.duration,
            'repetition': self.repetition,
            'subject_shortcut': self.subject_shortcut,
        }


class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    teaching_activity_id = db.Column(db.BigInteger, db.ForeignKey('teaching_activities.id'), nullable=False)
    room_id = db.Column(db.BigInteger, db.ForeignKey('rooms.id'), nullable=False)
    instructor_name = db.Column(db.String(255), db.ForeignKey('users.name'), nullable=False)
    day_and_time = db.Column(db.DateTime, nullable=False)
    check_room_collisions = db.Column(db.Boolean, default=False)
    check_schedule_requests = db.Column(db.Boolean, default=False)
    room = db.relationship('Room', back_populates='schedules')
    teaching_activity = db.relationship('TeachingActivity', back_populates='schedules')



