Create DATABASE iisdatabase;
USE iisdatabase;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  password VARCHAR(255),
  role VARCHAR(255)
);

CREATE TABLE rooms (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255),
  capacity INT
);

CREATE TABLE Subjects (
  ID SERIAL PRIMARY KEY,
  Shortcut VARCHAR(255) UNIQUE NOT NULL,
  Name VARCHAR(255) NOT NULL,
  Annotation TEXT,
  Credits INT,
  ID_Guarantor INT REFERENCES Users(ID)
);
CREATE TABLE TeachingActivities (
  ID SERIAL PRIMARY KEY,
  Label VARCHAR(255),
  Duration INT,
  Repetition VARCHAR(255),
  ID_Subject INT REFERENCES Subjects(ID)
);
CREATE TABLE SubjectGuardians (
  ID_Subject INT REFERENCES Subjects(ID),
  ID_Teacher INT REFERENCES Users(ID),
  PRIMARY KEY (ID_Subject, ID_Teacher)
);
CREATE TABLE CourseInstructors (
  ID_Teacher INT REFERENCES Users(ID),
  ID_Subject INT REFERENCES Subjects(ID),
  PRIMARY KEY (ID_Teacher, ID_Subject)
);
CREATE TABLE TeacherPersonalPreferences (
  ID SERIAL PRIMARY KEY,
  ID_User INT REFERENCES Users(ID),
  SatisfactoryDaysAndTimes TEXT
);
CREATE TABLE Schedule (
  ID SERIAL PRIMARY KEY,
  ID_TeachingActivity INT REFERENCES TeachingActivities(ID),
  ID_Room INT REFERENCES Rooms(ID),
  ID_Instructor INT REFERENCES Users(ID),
  DayAndTime DATETIME,
  CheckRoomCollisions BOOLEAN,
  CheckScheduleRequests BOOLEAN
);
CREATE TABLE PersonalStudentSchedule (
  ID SERIAL PRIMARY KEY,
  ID_User INT REFERENCES Users(ID),
  ID_TeachingActivity INT REFERENCES TeachingActivities(ID)
);
CREATE TABLE SubjectAnnotations (
  ID SERIAL PRIMARY KEY,
  ID_Subject INT REFERENCES Subjects(ID),
  Annotation TEXT
);


-- Insert test data into the users table
INSERT INTO users (name, password, role) VALUES
  ('Admin User', 'adminpass', 'administrator'),
  ('Garant User', 'garantpass', 'garant předmětu'),
  ('Teacher User', 'teacherpass', 'vyučující'),
  ('Room User', 'roompass', 'rozvrhář'),
  ('Student User', 'studentpass', 'student'),
  ('Unregistered User', 'unregpass', 'neregistrovaný');

-- Insert test data into the rooms table
INSERT INTO rooms (title, capacity) VALUES
  ('Room A', 30),
  ('Room B', 20),
  ('Room C', 25);

-- Insert test data into the Subjects table
INSERT INTO Subjects (Shortcut, Name, Annotation, Credits, ID_Guarantor) VALUES
  ('MATH101', 'Mathematics 101', 'Introduction to basic math concepts', 3, 2),
  ('PHYS101', 'Physics 101', 'Fundamental principles of physics', 3, 3),
  ('CHEM101', 'Chemistry 101', 'Basic chemistry concepts', 3, 3);

-- Insert test data into the TeachingActivities table
INSERT INTO TeachingActivities (Label, Duration, Repetition, ID_Subject) VALUES
  ('Lecture 1', 90, 'every week', 1),
  ('Lab 1', 120, 'every week', 2),
  ('Seminar 1', 90, 'odd weeks', 3);

-- Insert test data into the SubjectGuardians table
INSERT INTO SubjectGuardians (ID_Subject, ID_Teacher) VALUES
  (1, 3),
  (2, 4),
  (3, 4);

-- Insert test data into the CourseInstructors table
INSERT INTO CourseInstructors (ID_Teacher, ID_Subject) VALUES
  (3, 1),
  (4, 2),
  (4, 3);

-- Insert test data into the TeacherPersonalPreferences table
INSERT INTO TeacherPersonalPreferences (ID_User, SatisfactoryDaysAndTimes) VALUES
  (3, 'Monday morning, Wednesday afternoon'),
  (4, 'Tuesday morning, Thursday afternoon');

-- Insert test data into the Schedule table
INSERT INTO Schedule (ID_TeachingActivity, ID_Room, ID_Instructor, DayAndTime, CheckRoomCollisions, CheckScheduleRequests) VALUES
  (1, 1, 3, '2023-10-16 09:00:00', false, true),
  (2, 2, 4, '2023-10-17 13:00:00', false, true),
  (3, 3, 4, '2023-10-18 10:00:00', false, true);

-- Insert test data into the PersonalStudentSchedule table
INSERT INTO PersonalStudentSchedule (ID_User, ID_TeachingActivity) VALUES
  (5, 1),
  (5, 3);

-- Insert test data into the SubjectAnnotations table
INSERT INTO SubjectAnnotations (ID_Subject, Annotation) VALUES
  (1, 'This course covers basic math topics.'),
  (2, 'Introduction to fundamental physics principles.'),
  (3, 'Learn the basics of chemistry.');

