CREATE DATABASE iisdatabase;
USE iisdatabase;

CREATE TABLE users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    password VARCHAR(255),
    role INT,
    PRIMARY KEY (id)
);

CREATE TABLE rooms (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    title VARCHAR(255),
    capacity INT,
    PRIMARY KEY (id)
);

CREATE TABLE subjects (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    shortcut VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    annotation TEXT,
    credits INT,
    id_guarantor BIGINT UNSIGNED,
    PRIMARY KEY (id),
    FOREIGN KEY (id_guarantor) REFERENCES users (id)
);

CREATE TABLE teaching_activities (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    label VARCHAR(255),
    duration INT,
    repetition VARCHAR(255),
    id_subject BIGINT UNSIGNED,
    PRIMARY KEY (id),
    FOREIGN KEY (id_subject) REFERENCES subjects (id)
);

CREATE TABLE subject_guardians (
    id_subject BIGINT UNSIGNED,
    id_teacher BIGINT UNSIGNED,
    PRIMARY KEY (id_subject, id_teacher),
    FOREIGN KEY (id_subject) REFERENCES subjects (id),
    FOREIGN KEY (id_teacher) REFERENCES users (id)
);

CREATE TABLE course_instructors (
    id_teacher BIGINT UNSIGNED,
    id_subject BIGINT UNSIGNED,
    PRIMARY KEY (id_teacher, id_subject),
    FOREIGN KEY (id_teacher) REFERENCES users (id),
    FOREIGN KEY (id_subject) REFERENCES subjects (id)
);

CREATE TABLE teacher_personal_preferences (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_user BIGINT UNSIGNED,
    satisfactory_days_and_times TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_user) REFERENCES users (id)
);

CREATE TABLE schedule (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_teaching_activity BIGINT UNSIGNED,
    id_room BIGINT UNSIGNED,
    id_instructor BIGINT UNSIGNED,
    day_and_time DATETIME,
    check_room_collisions BOOLEAN,
    check_schedule_requests BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (id_teaching_activity) REFERENCES teaching_activities (id),
    FOREIGN KEY (id_room) REFERENCES rooms (id),
    FOREIGN KEY (id_instructor) REFERENCES users (id)
);

CREATE TABLE personal_student_schedule (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    id_user BIGINT UNSIGNED,
    id_teaching_activity BIGINT UNSIGNED,
    PRIMARY KEY (id),
    FOREIGN KEY (id_user) REFERENCES users (id),
    FOREIGN KEY (id_teaching_activity) REFERENCES teaching_activities (id)
);

-- Insert test data into the users table
-- Assuming the 'role' field represents some sort of role ID (enumeration).
INSERT INTO users (name, password, role) VALUES
    ('Admin User', 'adminpass', 1),        -- Assuming 1 represents 'administrator'
    ('Garant User', 'garantpass', 2),      -- Assuming 2 represents 'garant předmětu'
    ('Teacher User', 'teacherpass', 3),    -- Assuming 3 represents 'vyučující'
    ('Room User', 'roompass', 4),          -- Assuming 4 represents 'rozvrhář'
    ('Student User', 'studentpass', 5),    -- Assuming 5 represents 'student'
    ('Unregistered User', 'unregpass', 6); -- Assuming 6 represents 'neregistrovaný'

-- Insert test data into the rooms table
INSERT INTO rooms (title, capacity) VALUES
    ('Room A', 30),
    ('Room B', 20),
    ('Room C', 25);

-- Insert test data into the subjects table
-- The values for ID_Guarantor must match an 'id' in the 'users' table. Adjust as necessary.
INSERT INTO subjects (shortcut, name, annotation, credits, id_guarantor) VALUES
    ('MATH101', 'Mathematics 101', 'Introduction to basic math concepts', 3, 1),
    ('PHYS101', 'Physics 101', 'Fundamental principles of physics', 3, 2),
    ('CHEM101', 'Chemistry 101', 'Basic chemistry concepts', 3, 2);

-- Insert test data into the teaching_activities table
INSERT INTO teaching_activities (label, duration, repetition, id_subject) VALUES
    ('Lecture 1', 90, 'every week', 1),
    ('Lab 1', 120, 'every week', 2),
    ('Seminar 1', 90, 'odd weeks', 3);

-- Insert test data into the subject_guardians table
INSERT INTO subject_guardians (id_subject, id_teacher) VALUES
    (1, 3),
    (2, 3),
    (3, 3);

-- Insert test data into the course_instructors table
INSERT INTO course_instructors (id_teacher, id_subject) VALUES
    (3, 1),
    (3, 2),
    (3, 3);

-- Insert test data into the teacher_personal_preferences table
INSERT INTO teacher_personal_preferences (id_user, satisfactory_days_and_times) VALUES
    (3, 'Monday morning, Wednesday afternoon'),
    (3, 'Tuesday morning, Thursday afternoon');

-- Insert test data into the schedule table
INSERT INTO schedule (id_teaching_activity, id_room, id_instructor, day_and_time, check_room_collisions, check_schedule_requests) VALUES
    (1, 1, 3, '2023-10-16 09:00:00', false, true),
    (2, 2, 3, '2023-10-17 13:00:00', false, true),
    (3, 3, 3, '2023-10-18 10:00:00', false, true);

-- Insert test data into the personal_student_schedule table
INSERT INTO personal_student_schedule (id_user, id_teaching_activity) VALUES
    (5, 1),
    (5, 3);
