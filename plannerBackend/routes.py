import os
from os.path import join, dirname
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from db import Subject, User, db, Room, SubjectGuardians, TeachingActivity, Schedule, Course_Instructors, \
    Teacher_Personal_Preferences
from db import User, db
from functools import wraps
from sqlalchemy.orm.exc import NoResultFound
from flask import request, jsonify
from datetime import datetime

my_routes = Blueprint('my_routes', __name__)


def login_required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id") or session.get("user_role") != 1:
            return render_template('views/admin/adminview.html', error='You are unauthorized.')
        return f(*args, **kwargs)
    return decorated_function


def login_required_teacher(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id") or session.get("user_role") != 1 and session.get("user_role") != 3 and session.get("user_role") != 2:
            return render_template('views/admin/adminview.html', error='You are unauthorized.')
        return f(*args, **kwargs)
    return decorated_function


def login_required_scheduler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id") or session.get("user_role") != 1:
            return render_template('views/admin/adminview.html', error='You are unauthorized.')
        return f(*args, **kwargs)
    return decorated_function


def login_required_guarantor(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id") or session.get("user_role") != 1 and session.get("user_role") != 2:
            return render_template('views/admin/adminview.html', error='You are unauthorized.')
        return f(*args, **kwargs)
    return decorated_function


def login_required_student(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id") or session.get("user_role") != 5:
            return render_template('views/admin/adminview.html', error='You are unauthorized.')
        return f(*args, **kwargs)
    return decorated_function

@my_routes.route('/login_view', methods=['GET'])
def login_view():
    return render_template('login.html')


@my_routes.route('/createUser', methods=['POST'])
def create_user():
    """
        Create a new user
        ---
        tags:
          - User Management
        parameters:
          - name: name
            in: body
            type: string
            required: true
          - name: password
            in: body
            type: string
            required: true
          - name: role
            in: body
            type: integer
            required: true
        responses:
          201:
            description: User successfully created
          500:
            description: Error in user creation
        """
    data = request.get_json()

    # Assuming your JSON data includes 'name', 'password', and 'role' fields
    new_user = User(name=data['name'], password=generate_password_hash(data['password']), role=5)

    try:
        db.session.add(new_user)
        db.session.commit()
        return render_template('views/admin/admCreateUser.html')
    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/admCreateUser.html', error="An unexpected error occurred. Please try again.")


@my_routes.route('/login', methods=['POST'])
def login():
    username = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(name=username).first()

    if user and check_password_hash(user.password, password):
        session.permanent = True
        session['user_id'] = user.id
        session['user_name'] = user.name
        session['user_role'] = user.role
        return render_template('views/admin/adminview.html')
    else:
        return 'Invalid username or password', 401


@my_routes.route('/admViewReroute', methods=['GET', 'POST'])
def admin_view_reroute():
    return render_template('views/admin/adminview.html')


@my_routes.route('/studentViewReroute', methods=['GET', 'POST'])
def student_view_reroute():
    schedule = get_schedule()
    activities = get_teaching_activities()
    rooms=get_rooms()
    return render_template('views/studentview.html', schedule=schedule, activities=activities, rooms=rooms)

@my_routes.route('/createCourseInstructorReroute', methods=['GET', 'POST'])
@login_required_guarantor
def create_course_instructor_reroute():
    teachers_list = get_teachers_and_garants()
    subjects_list = get_subjects()
    return render_template('views/admin/admAddTeacherToSubject.html', teachers=teachers_list, subjects=subjects_list)


@my_routes.route('/createUserReroute', methods=['GET', 'POST'])
@login_required_admin
def create_user_reroute():
    return render_template('views/admin/admCreateUser.html')


@my_routes.route('/updateUserReroute', methods=['GET', 'POST'])
@login_required_admin
def update_user_reroute():
    users_list = get_users()
    return render_template('views/admin/admUpdateUser.html', users=users_list)


@my_routes.route('/updateSubjectReroute', methods=['GET', 'POST'])
@login_required_admin
def update_subject_reroute():
    subject_list = get_subjects()
    guarantors = get_garants()
    return render_template('views/admin/admUpdateSubject.html', subjects=subject_list, guarantors=guarantors)


@my_routes.route('/setSubjectGuarantorReroute', methods=['GET', 'POST'])
@login_required_admin
def set_subject_guarantor_reroute():
    subject_list = get_subjects()
    guarantor_list = get_garants()
    return render_template('views/admin/admSetGuarantorOfSubject.html', subjects=subject_list, guarantors=guarantor_list)


@my_routes.route('/setTeacherPreferencesReroute', methods=['GET', 'POST'])
@login_required_teacher
def set_teacher_preferences_reroute():
    if session.get('user_role') == 1:
        teachers_list = get_teachers_and_garants()
    else:
        teachers_list = [{'name': session.get('user_name')}]
    return render_template('views/admin/admDefinePreferences.html', teachers=teachers_list)


@my_routes.route('/createSubjectReroute', methods=['GET', 'POST'])
@login_required_admin
def create_subject_reroute():
    guarantors = get_garants()
    return render_template('views/admin/admAddSubject.html', guarantors=guarantors)


@my_routes.route('/createRoomReroute', methods=['GET', 'POST'])
@login_required_admin
def create_room_reroute():
    return render_template('views/admin/admCreateRoom.html')


@my_routes.route('/createTeachingActivityReroute', methods=['GET', 'POST'])
@login_required_guarantor
def create_teaching_activity_reroute():
    teaching_list = get_subjects()
    return render_template('views/admin/admAddTeachingActivity.html', activities=teaching_list)


@my_routes.route('/deleteTeachingActivityReroute', methods=['GET', 'POST'])
@login_required_guarantor
def delete_teaching_activity_reroute():
    teaching_list = get_teaching_activities()
    return render_template('views/admin/admDeleteTeachingActivity.html', teaching_list=teaching_list)


@my_routes.route('/deleteCourseInstructorReroute', methods=['GET', 'POST'])
@login_required_guarantor
def delete_teacher_from_subject_reroute():
    subjects_list = get_subjects()
    return render_template('views/admin/admDeleteTeacherFromSubject.html', subjects_list=subjects_list)


@my_routes.route('/deleteUserReroute', methods=['GET', 'POST'])
@login_required_admin
def delete_user_reroute():
    users_list = get_users()
    return render_template('views/admin/admDeleteUser.html', users=users_list)


@my_routes.route('/deleteRoomReroute', methods=['GET', 'POST'])
@login_required_admin
def delete_room_reroute():
    room_list = get_rooms()
    return render_template('views/admin/admDeleteRoom.html', rooms=room_list)


@my_routes.route('/deleteSubjectReroute', methods=['GET', 'POST'])
@login_required_admin
def delete_subject_reroute():
    subject_list = get_subjects()
    return render_template('views/admin/admDeleteSubject.html', subjects=subject_list)


@my_routes.route('/addTeachingActivityInScheduleReroute', methods=['GET', 'POST'])
@login_required_scheduler
def add_teaching_activity_in_schedule_reroute():
    activities_list = get_teaching_activities()
    rooms_list = get_rooms()
    instructors_list = get_course_instructors()
    return render_template('views/admin/admAddActivityInSchedule.html', activities=activities_list, rooms=rooms_list, instructors=instructors_list)


@my_routes.route('/getInstructorsForActivityReroute', methods=['GET', 'POST'])
def get_instructor_for_activity_reroute():
    rooms_list = get_rooms()
    activities_list = get_teaching_activities()
    instructors, activities = get_course_instructors_ta()
    return render_template('views/admin/admAddActivityInSchedule.html', activities=activities_list, instructors=instructors, picked_activities=activities, rooms=rooms_list)


@my_routes.route('/getInstructorsForCourseReroute', methods=['GET', 'POST'])
def get_instructor_for_course_reroute():
    subjects_list = get_subjects()
    instructors, subjects = get_course_instructors_subject()
    return render_template('views/admin/admDeleteTeacherFromSubject.html', subjects_list=subjects_list, instructors=instructors, picked_subject=subjects)


@my_routes.route('/deleteTeachingActivityFromScheduleReroute', methods=['GET', 'POST'])
@login_required_scheduler
def delete_teaching_activity_from_schedule_reroute():
    activities_list = get_schedule()
    return render_template('views/admin/admDeleteTeachingActivityFromSchedule.html', teaching_list=activities_list)


@my_routes.route('/getCourseInstructorsSubject', methods=['GET', 'POST'])
def get_course_instructors_subject():
    try:
        shortcut_req = request.form.get('shortcut')

        course_instructors = Course_Instructors.query.filter_by(shortcut=shortcut_req).all()
        subjects = Subject.query.filter_by(shortcut=shortcut_req).all()

        # Convert the list of Course_Instructors objects to a list of dictionaries
        instructors_list = [{'teacher_name': instructor.teacher_name, 'shortcut': instructor.shortcut} for instructor in course_instructors]
        subjects_list = [{'name': subject.name, 'annotation': subject.annotation, 'shortcut': subject.shortcut, 'credits': subject.credits, 'guarantor_name': subject.guarantor_name} for subject in subjects]

        # Return the list in JSON format
        return instructors_list, subjects_list
    except Exception as e:
        # In case of an exception, return an error message
        return render_template('views/admin/adminview.html', error="Unexpected Error")


@my_routes.route('/logout', methods=['GET', 'POST'])
def logout():
    # Clear the user's session
    session.clear()
    # Redirect to the login page, or to the home page, as preferred
    return render_template('login.html')

########################################################################################
##subject routes


@my_routes.route('/addSubject', methods=['POST', 'GET'])
@login_required_admin
def add_subject():
    shortcut = request.form.get('shortcut')
    name = request.form.get('name')
    annotation = request.form.get('annotation')
    credits = request.form.get('credits')
    guarantor_name = request.form.get('id_guarantor')
    try:
        # Ensure the guarantor exists before adding the subject
        guarantor = User.query.filter_by(name=guarantor_name).first()
        if guarantor is None:
            return render_template('views/admin/admAddSubject.html', error="Guarantor doesn't exist. Please try again.")

        new_subject = Subject(
            shortcut=shortcut,
            name=name,
            annotation=annotation,
            credits=credits,
            guarantor_name=guarantor_name  # Use the guarantor's name as the foreign key
        )

        db.session.add(new_subject)
        db.session.commit()
        return render_template('views/admin/admAddSubject.html')

    except IntegrityError as e:
        db.session.rollback()
        # Check if it's a duplicate entry error
        if 'Duplicate entry' in str(e):
            friendly_error = "This subject already exists. Please use a different shortcut."
        else:
            friendly_error = "A database error occurred. Please try again."
        return render_template('views/admin/admAddSubject.html', error=friendly_error)
    except Exception as e:
        db.session.rollback()
        # For other types of errors, you might want to log them or handle them differently
        return render_template('views/admin/admAddSubject.html', error="An unexpected error occurred. Please try again.")


@my_routes.route('/deleteSubject', methods=['DELETE', 'POST', 'GET'])
def delete_subject():
    shortcut = request.form.get('old_shortcut')
    try:
        subject = Subject.query.filter_by(shortcut=shortcut).first()
        if subject:
            # Check for related subject_guardians entries
            related_guardians = SubjectGuardians.query.filter_by(shortcut=shortcut).all()

            if related_guardians:
                # Option 1: Delete related subject_guardians entries
                for guardian in related_guardians:
                    db.session.delete(guardian)

            db.session.delete(subject)
            db.session.commit()
            return redirect('/deleteSubjectReroute')  # No content
        else:
            return render_template('views/admin/admDeleteSubject.html', error='Subject not found')
    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/admDeleteSubject.html', error=str(e))


@my_routes.route('/updateSubject', methods=['POST', 'GET'])
def update_subject():
    db.session.rollback()
    new_shortcut = request.form.get('new_shortcut')
    old_shortcut = request.form.get('old_shortcut')
    annotation = request.form.get('annotation')
    name = request.form.get('name')
    credits = request.form.get('credits')
    guarantor_name = request.form.get('id_guarantor')

    subject = Subject.query.filter_by(shortcut=old_shortcut).first()

    if subject is None:
        return render_template('views/admin/admUpdateSubject.html', error='Subject not found')

    try:
        if new_shortcut:
            subject.shortcut = new_shortcut
        if annotation:
            subject.annotation = annotation
        if credits:
            subject.credits = credits
        if guarantor_name:
            subject.guarantor_name = guarantor_name
        if name:
            subject.name = name

        db.session.commit()
        return redirect('/updateSubjectReroute')

    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/admUpdateSubject.html',
                               error="An unexpected error occurred. Please try again.")


######################################################################################
###ROOMS ROUTES


@my_routes.route('/createRoomAdmin', methods=['POST'])
def create_room_admin():
    title = request.form.get('room_title')
    room_capacity = request.form.get('room_capacity')
    try:
        exists = Room.query.filter_by(title=title).first()
        if exists:
            return render_template('views/admin/admCreateRoom.html', error="This room doesnt exists. Please use a different name.")
        new_room = Room(
            title=title,
            capacity=room_capacity
        )
        db.session.add(new_room)
        db.session.commit()
        return render_template('views/admin/admCreateRoom.html')
    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/admCreateRoom.html', error="An unexpected error occurred. Please try again.")


@my_routes.route('/deleteRoomAdmin', methods=['DELETE', 'POST', 'GET'])
def delete_room_admin():
    room_title = request.form.get('title')
    room_to_delete = Room.query.filter_by(title=room_title).first()

    if room_to_delete is None:
        # If no room is found, return a 404 error
        return render_template('views/admin/admCreateRoom.html',
                               error="The room doesnt exist Please try again.")

    try:
        # If the room is found, delete it from the database
        db.session.delete(room_to_delete)
        db.session.commit()
        # Return a 200 status code to indicate success
        return redirect('/deleteRoomReroute')
    except Exception as e:
        # If there's an error during the deletion, rollback the session
        db.session.rollback()
        print(f"Error: {e}")
        # Return a 500 internal server error status code
        return render_template('views/admin/admDeleteRoom.html',
                               error="An unexpected error occurred. Please try again.")


######################################################################################
###Admin Routes
from sqlalchemy.exc import IntegrityError


@my_routes.route('/createUserAdmin', methods=['POST', 'GET'])
def create_user_admin():
    name = request.form.get('name')
    password = request.form.get('password')
    role = request.form.get('role')
    try:
        user = User.query.filter_by(name=name).first()
        if user is not None:
            return render_template('views/admin/adminview.html', error="This user already exists. Please use a different name.")
        new_user = User(
            name=name,
            password=generate_password_hash(password),
            role=role
        )

        db.session.add(new_user)
        db.session.commit()
        # Redirect or render success page/template
        return render_template('views/admin/admCreateUser.html')
    except Exception as e:
        db.session.rollback()
        # For other types of errors, handle them appropriately
        return render_template('views/admin/adminview.html', error="An unexpected error occurred. Please try again.")


@my_routes.route('/updateUserAdmin', methods=['POST', 'GET'])
def update_user_admin():
    # Handle form submission for updating user details
    old_name = request.form.get('old_name')
    new_name = request.form.get('new_name')
    password = request.form.get('password')
    role = request.form.get('role')

    user = User.query.filter_by(name=old_name).first()
    if user is None:
        return render_template('views/admin/admUpdateUser.html', error='User not found')

    try:
        if new_name:
            user.name = new_name
        if password:
            user.password = generate_password_hash(password)
        if role:
            user.role = role
        db.session.commit()
        return redirect('/updateUserReroute')
    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/admUpdateUser.html',
                               error="An unexpected error occurred. Please try again.")


@my_routes.route('/deleteUserAdmin', methods=['DELETE', 'POST', 'GET'])
def delete_user_admin():
    name = request.form.get('name')
    try:
        user = User.query.filter_by(name=name).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return redirect('/deleteUserReroute')
        else:
            return render_template('views/admin/admDeleteUser.html', error='User not found')
    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/admDeleteUser.html', error="Unexpected Error")

######################################################################################


@my_routes.route('/setGuarantorOfSubject', methods=['POST'])
def set_guarantor_of_subject():
    """
        Set or update the guarantor of a subject
        ---
        tags:
          - Subject Management
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - shortcut
                - guarantor_name
              properties:
                shortcut:
                  type: string
                  description: The shortcut of the subject
                guarantor_name:
                  type: string
                  description: The name of the new guarantor
        responses:
          200:
            description: Guarantor updated successfully
          404:
            description: Subject or new guarantor not found
          500:
            description: Internal server error
        """
    subject_shortcut = request.form.get('shortcut')
    new_guarantor_name = request.form.get('name')

    # Check if the subject exists
    subject = Subject.query.filter_by(shortcut=subject_shortcut).first()
    if not subject:
        return render_template('views/admin/adminview.html',
                               error="Shortcut doesn't exist. Please try again.")

    # Check if the new guarantor exists
    new_guarantor = User.query.filter_by(name=new_guarantor_name).first()
    if not new_guarantor:
        return render_template('views/admin/adminview.html',
                               error="Subject doesn't exist. Please try again.")

    # Update the guarantor of the subject
    subject.guarantor_name = new_guarantor_name

    try:
        db.session.commit()
        return redirect('/setSubjectGuarantorReroute')
    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")

######################################################################################


@my_routes.route('/addTeachingActivity', methods=['POST'])
def add_teaching_activity():
    """
        Add a new teaching activity
        ---
        tags:
          - Teaching Activities
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - label
                - duration
                - repetition
                - subject_shortcut
              properties:
                label:
                  type: string
                  description: Label of the teaching activity
                duration:
                  type: integer
                  description: Duration of the activity
                repetition:
                  type: string
                  description: Repetition pattern of the activity
                subject_shortcut:
                  type: string
                  description: The subject's shortcut associated with the activity
        responses:
          201:
            description: Teaching activity added successfully
          404:
            description: Subject not found
          500:
            description: Internal server error
        """
    shortcut = request.form.get('subject_shortcut')
    label = request.form.get('label')
    duration = request.form.get('duration')
    repetition = request.form.get('repetition')
    preferences = request.form.get('preferences')

    # Validate data (optional, but recommended)
    # For example, check if the subject exists, the duration is a positive number, etc.

    try:
        querry = Subject.query.filter_by(shortcut=shortcut).first()
        if querry is None:
            return render_template('views/admin/adminview.html',
                                   error="Subject doesn't exist. Please try again.")

        new_teaching_activity = TeachingActivity(
            label=label,
            duration=duration,
            repetition=repetition,
            shortcut=shortcut,
            preference=preferences
        )
        # Add the new object to the database
        db.session.add(new_teaching_activity)
        db.session.commit()
        return redirect('/createTeachingActivityReroute')
    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")


@my_routes.route('/deleteTeachingActivity', methods=['DELETE', 'POST', 'GET'])
def delete_teaching_activity():
    label = request.form.get('label')
    """
        Delete a teaching activity by its label
        ---
        tags:
          - Teaching Activities
        parameters:
          - name: label
            in: path
            type: string
            required: true
            description: Label of the teaching activity to delete
        responses:
          200:
            description: Teaching activity deleted successfully
          404:
            description: Teaching activity not found
          500:
            description: Internal server error
        """
    try:
        teachingactivity = TeachingActivity.query.filter_by(label=label).first()
        if teachingactivity:

            db.session.delete(teachingactivity)
            db.session.commit()
            return redirect('/deleteTeachingActivityReroute')  # No content
        else:
            return render_template('views/admin/admDeleteTeachingActivity.html', error='Activity not found')
    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/admDeleteTeachingActivity.html', error=str(e))


@my_routes.route('/addTeacherToSubject', methods=['POST'])
def add_teacher_to_subject():
    name = request.form.get('name')
    shortcut = request.form.get('subject_shortcut')

    # Check if the teacher exists
    teacher = User.query.filter_by(name=name).first()
    if not teacher:
        return render_template('views/admin/adminview.html',
                               error="Teacher doesn't exist. Please try again.")

    # Check if the subject exists
    subject = Subject.query.filter_by(shortcut=shortcut).first()
    if not subject:
        return render_template('views/admin/adminview.html',
                               error="Shortcut doesn't exist. Please try again.")

    query = Course_Instructors.query.filter_by(teacher_name=name).all()

    # Find the entry with the matching shortcut
    matching_entry = next((entry for entry in query if entry.shortcut == shortcut), None)
    # Create a new CourseInstructors object
    if matching_entry:
        return render_template('views/admin/adminview.html',
                               error="This teacher is already assigned to this subject.")
    new_course_instructor = Course_Instructors(
        teacher_name=name,
        shortcut=shortcut
    )

    try:
        # Add the new object to the database
        db.session.add(new_course_instructor)
        db.session.commit()
        return redirect('/createCourseInstructorReroute')
    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/adminview.html',
                               error="Unexpected Error.")


@my_routes.route('/deleteTeacherFromSubject', methods=['POST', 'GET', 'DELETE'])
def delete_teacher_from_subject():
    # Retrieve form data
    shortcut = request.form.get('shortcut')
    name = request.form.get('name')

    try:
        # Query all entries for the given teacher name
        query = Course_Instructors.query.filter_by(teacher_name=name).all()

        # Find the entry with the matching shortcut
        matching_entry = next((entry for entry in query if entry.shortcut == shortcut), None)

        if matching_entry:
            # If a matching entry is found, delete it
            db.session.delete(matching_entry)
            db.session.commit()
            # Redirect or render success page/template
            return redirect('/deleteTeacherFromSubjectReroute')
        else:
            # If no matching entry is found, display an error
            return render_template('views/admin/admDeleteTeacherFromSubject.html', error='Teacher/subject not found')
    except Exception as e:
        # Handle any exceptions
        db.session.rollback()
        print(f"Unexpected error: {e}")  # Log the error for debugging
        return render_template('views/admin/adminview.html', error="An unexpected error occurred. Please try again.")


@my_routes.route('/definePreferences', methods=['POST'])
@login_required_teacher
def define_preferences():
    teacher_name = request.form.get('name')
    preferences = request.form.get('preferences')

    # Check if preferences already exist for the teacher
    existing_preferences = Teacher_Personal_Preferences.query.filter_by(teacher_name=teacher_name).first()

    if existing_preferences:
        # Update existing preferences
        existing_preferences.satisfactory_days_and_times = preferences
    else:
        # Create new preferences
        new_preferences = Teacher_Personal_Preferences(teacher_name=teacher_name, satisfactory_days_and_times=preferences)
        db.session.add(new_preferences)

    try:
        db.session.commit()
        return redirect('/setTeacherPreferencesReroute')
    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")


@my_routes.route('/addActivityInSchedule', methods=['POST'])
def add_activity_in_schedule():

    teaching_activity_label = request.form.get('picked_label')
    room_title = request.form.get('room_title')
    instructor_name = request.form.get('instructor_name')
    day = request.form.get('day')  # assuming this is passed as a string
    hour = request.form.get('hour')  # assuming this is passed as a string
    repetition = request.form.get('repetition')


    # Find the teaching activity by label
    teaching_activity = TeachingActivity.query.filter_by(label=teaching_activity_label).first()
    if not teaching_activity:
        return render_template('views/admin/adminview.html',
                               error="Teaching Activity not found.")

    # Find the room by title
    room = Room.query.filter_by(title=room_title).first()
    if not room:
        return render_template('views/admin/adminview.html',
                               error="Room not found.")

    # Create new schedule entry
    new_schedule_entry = Schedule(
        teaching_activity_id=teaching_activity.id,
        room_id=room.id,
        instructor_name=instructor_name,
        day=day,
        hour=hour,
        repetition=repetition,
        # Set check_room_collisions and check_schedule_requests if applicable
    )

    try:
        db.session.add(new_schedule_entry)
        db.session.commit()
        return redirect('/addTeachingActivityInScheduleReroute')
    except Exception as e:
        db.session.rollback()
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")


@my_routes.route('/getSchedule', methods=['GET'])
def get_schedule():
    try:
        # Query all schedule entries with related room and teaching activity details
        schedule_entries = Schedule.query.join(Room, Schedule.room_id == Room.id).join(TeachingActivity, Schedule.teaching_activity_id == TeachingActivity.id).all()

        # Convert the schedule entries to a JSON-friendly format with room and teaching activity names
        schedule_list = []
        for entry in schedule_entries:
            schedule_dict = {
                'id': entry.id,
                'room_name': entry.room.title if entry.room else 'N/A',
                'teaching_activity_name': entry.teaching_activity.label if entry.teaching_activity else 'N/A',
                'instructor_name': entry.instructor_name,
                'day': entry.day,
                'hour': entry.hour,
                'repetition': entry.teaching_activity.repetition if entry.teaching_activity else 'N/A',
                # include other fields as needed
            }
            schedule_list.append(schedule_dict)
            print(schedule_list)

        return schedule_list
    except Exception as e:
        print(f"Error: {e}")
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")



@my_routes.route('/getUsers', methods=['GET'])
def get_users():
    try:
        # Query all users
        users = User.query.all()

        # Convert the list of user objects to a list of dictionaries
        users_list = [user.as_dict() for user in users]

        # Return the list in JSON format
        return users_list
    except Exception as e:
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")

@my_routes.route('/getTeachersAndGarants', methods=['GET'])
def get_teachers_and_garants():
    try:
        # Query all users
        users = User.query.filter(User.role.in_([2, 3])).all()

        # Convert the list of user objects to a list of dictionaries
        users_list = [user.as_dict() for user in users]

        # Return the list in JSON format
        return users_list
    except Exception as e:
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")


@my_routes.route('/getGarants', methods=['GET'])
def get_garants():
    try:
        # Query all users
        users = User.query.filter(User.role.in_([2])).all()

        # Convert the list of user objects to a list of dictionaries
        users_list = [user.as_dict() for user in users]

        # Return the list in JSON format
        return users_list
    except Exception as e:
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")


@my_routes.route('/getSubjects', methods=['GET'])
def get_subjects():
    try:
        # Query all subjects from the database
        subjects = Subject.query.all()

        # Convert the list of Subject objects to a list of dictionaries
        subjects_list = [subject.as_dict() for subject in subjects]

        # Return the list in JSON format
        return subjects_list
    except Exception as e:
        # In case of an exception, return an error message
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")


@my_routes.route('/getRooms', methods=['GET'])
def get_rooms():
    try:
        # Query all rooms from the database
        rooms = Room.query.all()

        # Convert the list of Room objects to a list of dictionaries
        rooms_list = [room.as_dict() for room in rooms]

        # Return the list in JSON format
        return rooms_list
    except Exception as e:
        # In case of an exception, return an error message
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")


@my_routes.route('/getTeachingActivities', methods=['GET'])
def get_teaching_activities():
    try:
        # Query all teaching activities from the database
        teaching_activities = TeachingActivity.query.all()

        # Convert the list of TeachingActivity objects to a list of dictionaries
        teaching_activities_list = [activity.as_dict() for activity in teaching_activities]

        # Return the list in JSON format
        return teaching_activities_list
    except Exception as e:
        # In case of an exception, return an error message
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")

##getCourseInstructors


@my_routes.route('/getCourseInstructors', methods=['GET', 'POST'])
def get_course_instructors():
    try:
        # Query all course instructors from the database
        course_instructors = Course_Instructors.query.all()

        # Convert the list of Course_Instructors objects to a list of dictionaries
        instructors_list = [instructor.as_dict() for instructor in course_instructors]

        # Return the list in JSON format
        return instructors_list
    except Exception as e:
        # In case of an exception, return an error message
        return render_template('views/admin/adminview.html',
                               error="An unexpected error occurred. Please try again.")


@my_routes.route('/getCourseInstructorsTa', methods=['POST', 'GET'])
def get_course_instructors_ta():
    try:
        label_req = request.form.get('teaching_activity')
        activity = TeachingActivity.query.filter_by(label=label_req).first()
        # Query course instructors for a specific subject

        course_instructors = Course_Instructors.query.filter_by(shortcut=activity.shortcut).all()
        activities = TeachingActivity.query.filter_by(label=label_req).all()

        # Convert the list of Course_Instructors objects to a list of dictionaries
        instructors_list = [{'teacher_name': instructor.teacher_name, 'shortcut': instructor.shortcut} for instructor in course_instructors]
        activity_list = [{'label': activity.label, 'duration': activity.duration, 'repetition': activity.repetition, 'shortcut': activity.shortcut} for activity in activities]

        # Return the list in JSON format
        return instructors_list, activity_list
    except Exception as e:
        # In case of an exception, return an error message
        return render_template('views/admin/adminview.html',
                               error="Unexpected Error")


##getSubjectGuardians
@my_routes.route('/getSubjectGuardians', methods=['GET'])
def get_subject_guardians():
    try:
        # Query all subject guardians from the database
        subject_guardians = SubjectGuardians.query.all()

        # Convert the list of SubjectGuardians objects to a list of dictionaries
        guardians_list = [{'shortcut': guardian.shortcut, 'teacher_name': guardian.teacher_name} for guardian in subject_guardians]

        # Return the list in JSON format
        return guardians_list
    except Exception as e:
        # In case of an exception, return an error message
        return render_template('views/admin/adminview.html',
                               error="Unexpected Error")


@my_routes.route('/getTeacherPersonalPreferences', methods=['GET'])
def get_teacher_personal_preferences():
    try:
        # Query all teacher personal preferences from the database
        teacher_preferences = Teacher_Personal_Preferences.query.all()

        # Convert the list of Teacher_Personal_Preferences objects to a list of dictionaries
        preferences_list = [{'teacher_name': pref.teacher_name, 'satisfactory_days_and_times': pref.satisfactory_days_and_times} for pref in teacher_preferences]

        # Return the list in JSON format
        return preferences_list
    except Exception as e:
        # In case of an exception, return an error message
        return render_template('views/admin/adminview.html',
                               error="Unexpected Error")


@my_routes.route('/deleteTeachingActivityFromSchedule', methods=['POST', 'GET'])
def delete_teaching_activity_from_schedule():
    label = request.form.get('label')
    try:
        # Find the teaching activity by label
        teaching_activity = TeachingActivity.query.filter_by(label=label).first()

        if teaching_activity is None:
            return render_template('views/admin/adminview.html',
                               error="Room not found.")

        # Delete associated schedule entries
        Schedule.query.filter_by(teaching_activity_id=teaching_activity.id).delete()

        db.session.commit()
        return redirect('/deleteTeachingActivityFromScheduleReroute')
    except NoResultFound:
        db.session.rollback()
        return render_template('views/admin/adminview.html', error='Teaching activity not found')
    except ValueError as e:
        db.session.rollback()
        return render_template('views/admin/adminview.html', error=str(e))
    except Exception as e:
        db.session.rollback()
        # Log the error for debugging
        print(f"Unexpected error: {e}")
        return render_template('views/admin/adminview.html', error="An unexpected error occurred. Please try again.")