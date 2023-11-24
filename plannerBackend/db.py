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
    guarantor_name = db.Column(db.String(255), db.ForeignKey('users.name', onupdate='CASCADE', ondelete='CASCADE'))

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
    shortcut = db.Column(db.String(255), db.ForeignKey('subjects.shortcut', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    teacher_name = db.Column(db.String(255), db.ForeignKey('users.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)

    # Relationships
    subject = db.relationship('Subject', backref=db.backref('subject_guardians', cascade='all, delete'))
    teacher = db.relationship('User', backref=db.backref('subject_guardians', cascade='all, delete'))


class TeachingActivity(db.Model):
    __tablename__ = 'teaching_activities'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    label = db.Column(db.String(255))
    duration = db.Column(db.Integer)
    repetition = db.Column(db.String(255))
    shortcut = db.Column(db.String(255), db.ForeignKey('subjects.shortcut', ondelete='CASCADE', onupdate='CASCADE'))

    # Relationships
    schedules = db.relationship('Schedule', back_populates='teaching_activity')
    subject = db.relationship('Subject')

    def as_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'duration': self.duration,
            'repetition': self.repetition,
            'shortcut': self.shortcut,
        }


class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    teaching_activity_id = db.Column(db.BigInteger, db.ForeignKey('teaching_activities.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    room_id = db.Column(db.BigInteger, db.ForeignKey('rooms.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    instructor_name = db.Column(db.String(255), db.ForeignKey('users.name', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    day = db.Column(db.Integer, nullable=False)  # Assuming 'day' ranges from 0 to 6
    hour = db.Column(db.Integer, nullable=False)  # Assuming 'hour' ranges from 0 to 13
    repetition = db.Column(db.String(255))
    check_room_collisions = db.Column(db.Boolean, default=False)
    check_schedule_requests = db.Column(db.Boolean, default=False)
    room = db.relationship('Room', back_populates='schedules')
    teaching_activity = db.relationship('TeachingActivity', back_populates='schedules')

    def as_dict(self):
        return {
            'id': self.id,
            'teaching_activity_id': self.teaching_activity_id,
            'room_id': self.room_id,
            'instructor_name': self.instructor_name,
            'day': self.day,
            'hour': self.hour,
            'repetition': self.repetition,
        }


class Course_Instructors(db.Model):
    __tablename__ = 'course_instructors'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    teacher_name = db.Column(db.String(255), db.ForeignKey('users.name', ondelete='CASCADE', onupdate='CASCADE'))
    shortcut = db.Column(db.String(255), db.ForeignKey('subjects.shortcut', ondelete='CASCADE', onupdate='CASCADE'))

    teacher = db.relationship('User', backref=db.backref('course_instructors', cascade='all, delete'))
    subject = db.relationship('Subject', backref=db.backref('course_instructors', cascade='all, delete'))

    def as_dict(self):
        return {
            'id': self.id,
            'teacher_name': self.teacher_name,
            'shortcut': self.shortcut,
        }

class Teacher_Personal_Preferences(db.Model):
    __tablename__ = 'teacher_personal_preferences'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    teacher_name = db.Column(db.String(255), db.ForeignKey('users.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    satisfactory_days_and_times = db.Column(db.Text)

    def as_dict(self):
        return {
            'id': self.id,
            'teacher_name': self.teacher_name,
            'satisfactory_days_and_times': self.satisfactory_days_and_times
        }

