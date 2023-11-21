USE defaultdb;

-- Users Table
CREATE TABLE users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255),
    role INT,
    PRIMARY KEY (id)
);

-- Rooms Table
CREATE TABLE rooms (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    title VARCHAR(255),
    capacity INT,
    PRIMARY KEY (id)
);

-- Subjects Table
CREATE TABLE subjects (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    shortcut VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    annotation TEXT,
    credits INT,
    guarantor_name VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (guarantor_name) REFERENCES users (name) ON DELETE CASCADE
);

-- Teaching Activities Table
CREATE TABLE teaching_activities (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    label VARCHAR(255),
    duration INT,
    repetition VARCHAR(255),
    shortcut VARCHAR(255),
    PRIMARY KEY (id),
    FOREIGN KEY (shortcut) REFERENCES subjects (shortcut) ON DELETE CASCADE
);

-- Subject Guardians Table
CREATE TABLE subject_guardians (
    shortcut varchar(255),
    teacher_name VARCHAR(255),
    PRIMARY KEY (shortcut, teacher_name),
    FOREIGN KEY (shortcut) REFERENCES subjects (shortcut) ON DELETE CASCADE,
    FOREIGN KEY (teacher_name) REFERENCES users (name) ON DELETE CASCADE
);

-- Course Instructors Table
CREATE TABLE course_instructors (
    teacher_name VARCHAR(255),
    shortcut varchar(255),
    PRIMARY KEY (teacher_name, shortcut),
    FOREIGN KEY (teacher_name) REFERENCES users (name) ON DELETE CASCADE,
    FOREIGN KEY (shortcut) REFERENCES subjects (shortcut) ON DELETE CASCADE
);

-- Teacher Personal Preferences Table
CREATE TABLE teacher_personal_preferences (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    teacher_name VARCHAR(255),
    satisfactory_days_and_times TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (teacher_name) REFERENCES users (name) ON DELETE CASCADE
);

-- Schedule Table
CREATE TABLE schedule (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    teaching_activity_id BIGINT UNSIGNED,
    room_id BIGINT UNSIGNED,
    instructor_name VARCHAR(255),
    day INT UNSIGNED check ( day between 0 and 6),
    hour INT UNSIGNED check ( hour between 0 and 13),
    repetition VARCHAR(255),
    check_room_collisions BOOLEAN,
    check_schedule_requests BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (teaching_activity_id) REFERENCES teaching_activities (id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms (id) ON DELETE CASCADE,
    FOREIGN KEY (instructor_name) REFERENCES users (name) ON DELETE CASCADE
);

-- Personal Student Schedule Table
CREATE TABLE personal_student_schedule (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    student_name VARCHAR(255),
    teaching_activity_id BIGINT UNSIGNED,
    PRIMARY KEY (id),
    FOREIGN KEY (student_name) REFERENCES users (name) ON DELETE CASCADE,
    FOREIGN KEY (teaching_activity_id) REFERENCES teaching_activities (id) ON DELETE CASCADE
);

INSERT INTO users (name, password, role) VALUES
    ('admin', 'admin', 1),        -- Assuming 1 represents 'administrator'
    ('garant', 'admin', 2),      -- Assuming 2 represents 'garant předmětu'
    ('teacher', 'admin', 3),    -- Assuming 3 represents 'vyučující'
    ('room', 'admin', 4),          -- Assuming 4 represents 'rozvrhář'
    ('student', 'admin', 5);    -- Assuming 5 represents 'student'


INSERT INTO rooms (title, capacity) VALUES
    ('Room A', 30),
    ('Room B', 20),
    ('Room C', 25);


-- Insert test data into the subjects table
-- The values for guarantor_name must match a 'name' in the 'users' table. Adjust as necessary.
INSERT INTO subjects (shortcut, name, annotation, credits, guarantor_name) VALUES
    ('MATH101', 'Mathematics 101', 'Introduction to basic math concepts', 3, 'admin'),
    ('PHYS101', 'Physics 101', 'Fundamental principles of physics', 3, 'garant'),
    ('CHEM101', 'Chemistry 101', 'Basic chemistry concepts', 3, 'garant');

-- Insert test data into the teaching_activities table
-- The values for id_subject must now correspond to the name of the subject
INSERT INTO teaching_activities (label, duration, repetition, shortcut) VALUES
    ('Lecture 1', 90, 'every week', 'MATH101'),
    ('Lab 1', 120, 'every week', 'PHYS101'),
    ('Seminar 1', 90, 'odd weeks', 'CHEM101');

-- Insert test data into the subject_guardians table
-- The values for id_subject and id_teacher must correspond to the subject name and teacher name
INSERT INTO subject_guardians (shortcut, teacher_name) VALUES
    ('MATH101', 'teacher'),
    ('PHYS101', 'teacher'),
    ('CHEM101', 'teacher');

-- Insert test data into the course_instructors table
-- The values for id_teacher and id_subject must correspond to the teacher name and subject name
INSERT INTO course_instructors (teacher_name, shortcut) VALUES
    ('teacher', 'MATH101'),
    ('teacher', 'PHYS101'),
    ('teacher', 'CHEM101');

-- Insert test data into the teacher_personal_preferences table
INSERT INTO teacher_personal_preferences (teacher_name, satisfactory_days_and_times) VALUES
    ('teacher', 'Monday morning, Wednesday afternoon'),
    ('teacher', 'Tuesday morning, Thursday afternoon');

-- Insert test data into the schedule table
-- Note: The values for id_teaching_activity, id_room, id_instructor need to be adjusted to new table structure
-- Assuming these values still refer to the auto-generated IDs for teaching_activities, rooms, and users tables
INSERT INTO schedule (teaching_activity_id, room_id, instructor_name, day, hour, repetition, check_room_collisions, check_schedule_requests) VALUES
    (1, 1, 'teacher', '1', '2', 'weekly',false, true),
    (2, 2, 'teacher', '2','3', 'daily',false, true),
    (3, 3, 'teacher', '3', '8', 'every odd week',false, true);

-- Insert test data into the personal_student_schedule table
-- The value for id_user must correspond to the user's name
INSERT INTO personal_student_schedule (student_name, teaching_activity_id) VALUES
    ('student', 1),
    ('student', 3);
