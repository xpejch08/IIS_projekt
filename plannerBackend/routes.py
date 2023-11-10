from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import Subject, User, db, Room, SubjectGuardians, TeachingActivity, Schedule
from db import User, db
from sqlalchemy.orm.exc import NoResultFound

my_routes = Blueprint('my_routes', __name__)


@my_routes.route('/createUser', methods=['POST'])
def create_user():
    data = request.get_json()

    # Assuming your JSON data includes 'name', 'password', and 'role' fields
    new_user = User(name=data['name'], password=generate_password_hash(data['password']), role=5)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.as_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@my_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('name')
    password = data.get('password')

    # Find the user by username
    user = User.query.filter_by(name=username).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['user_name'] = user.name
        return jsonify({'success': True, 'user.role': user.role}), 200  # Redirecting to the path that serves the HTML file
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@my_routes.route('/getUser/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.as_dict()), 200
    except NoResultFound:
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@my_routes.route('/updateUser/<string:name>', methods=['PUT'])
def update_user(name):
    data = request.get_json()
    user = User.query.filter_by(name=name).first()

    if user is not None:
        # Update the user's attributes if they are provided in the JSON data
        if 'name' in data:
            user.name = data['name']
        if 'password' in data:
            hashed_password = generate_password_hash(data['password'])
            user.password = hashed_password
        if 'role' in data:
            user.role = data['role']

        try:
            db.session.commit()
            return jsonify(user.as_dict()), 200  # 200 for a successful update
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'User not found'}), 404  # 404 if the user with the specified name doesn't exist
########################################################################################
##subject routes


@my_routes.route('/addSubject', methods=['POST'])
def add_subject():
    data = request.get_json()
    guarantor_name = data['id_guarantor']  # Get the guarantor's name

    try:
        # Ensure the guarantor exists before adding the subject
        guarantor = User.query.filter_by(name=guarantor_name).first()
        if guarantor is None:
            return jsonify({'error': 'Guarantor user not found'}), 404

        new_subject = Subject(
            shortcut=data['shortcut'],
            name=data['name'],
            annotation=data.get('annotation', ''),
            credits=data['credits'],
            guarantor_name=guarantor_name  # Use the guarantor's name as the foreign key
        )

        db.session.add(new_subject)
        db.session.commit()
        return jsonify(new_subject.as_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@my_routes.route('/deleteSubject/<string:shortcut>', methods=['DELETE'])
def delete_subject(shortcut):
    try:
        subject = Subject.query.filter_by(shortcut=shortcut).first()
        if subject:
            # Check for related subject_guardians entries
            related_guardians = SubjectGuardians.query.filter_by(shortcut=shortcut).all()

            if related_guardians:
                # Option 1: Delete related subject_guardians entries
                for guardian in related_guardians:
                    db.session.delete(guardian)

                # Option 2: Update related subject_guardians entries
                # for guardian in related_guardians:
                #     guardian.subject_id = None  # or set to a new value
                #     db.session.add(guardian)

            db.session.delete(subject)
            db.session.commit()
            return jsonify({'success': 'Subject deleted'}), 204  # No content
        else:
            return jsonify({'error': 'Subject not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@my_routes.route('/getSubject/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):
    try:
        subject = Subject.query.get(subject_id)
        if subject:
            return jsonify(subject.as_dict()), 200
        else:
            return jsonify({'error': 'Subject not found'}), 404
    except NoResultFound:
        return jsonify({'error': 'Subject not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

######################################################################################
###ROOMS ROUTES


@my_routes.route('/createRoomAdmin', methods=['POST'])
def create_room_admin():
    data = request.get_json()
    new_room = Room(
        title=data['title'],
        capacity=data['capacity'],
    )
    try:
        db.session.add(new_room)
        db.session.commit()
        return jsonify(new_room.as_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@my_routes.route('/deleteRoomAdmin/<string:title>', methods=['DELETE'])
def delete_room_admin(title):
    # Attempt to find the room by its ID
    room_to_delete = Room.query.filter_by(title=title).first()

    if room_to_delete is None:
        # If no room is found, return a 404 error
        return jsonify({'error': 'Room not found'}), 404

    try:
        # If the room is found, delete it from the database
        db.session.delete(room_to_delete)
        db.session.commit()
        # Return a 200 status code to indicate success
        return jsonify({'success': 'Room deleted'}), 200
    except Exception as e:
        # If there's an error during the deletion, rollback the session
        db.session.rollback()
        print(f"Error: {e}")
        # Return a 500 internal server error status code
        return jsonify({'error': str(e)}), 500


######################################################################################
###Admin Routes
@my_routes.route('/createUserAdmin', methods=['POST'])
def create_user_admin():
    data = request.get_json()

    # Assuming your JSON data includes 'name', 'password', and 'role' fields
    new_user = User(name=data['name'], password=generate_password_hash(data['password']), role=data['role'])

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.as_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@my_routes.route('/updateUserAdmin/<string:name>', methods=['PUT'])
def update_user_admin(name):
    data = request.get_json()
    user = User.query.filter_by(name=name).first()

    if user is not None:
        # Update the user's attributes if they are provided in the JSON data
        if 'name' in data and data['name'] != "":
            user.name = data['name']
        if 'password' in data:
            hashed_password = generate_password_hash(data['password'])
            user.password = hashed_password
        if 'role' in data:
            user.role = data['role']

        try:
            db.session.commit()
            return jsonify(user.as_dict()), 200  # 200 for a successful update
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'User not found'}), 404  # 404 if the user with the specified name doesn't exist

@my_routes.route('/deleteUserAdmin/<string:name>', methods=['DELETE'])
def delete_user_admin(name):
    try:
        user = User.query.filter_by(name=name).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return jsonify(user.as_dict()), 204
        else:
            return jsonify({'error': 'No user named ' + name}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

######################################################################################


@my_routes.route('/setGuarantorOfSubject', methods=['PUT'])
def set_guarantor_of_subject():
    data = request.get_json()
    subject_shortcut = data.get('shortcut')
    new_guarantor_name = data.get('guarantor_name')

    # Check if the subject exists
    subject = Subject.query.filter_by(shortcut=subject_shortcut).first()
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404

    # Check if the new guarantor exists
    new_guarantor = User.query.filter_by(name=new_guarantor_name).first()
    if not new_guarantor:
        return jsonify({'error': 'New guarantor not found'}), 404

    # Update the guarantor of the subject
    subject.guarantor_name = new_guarantor_name

    try:
        db.session.commit()
        return jsonify({'success': 'Guarantor updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

######################################################################################


@my_routes.route('/addTeachingActivity', methods=['POST'])
def add_teaching_activity():
    data = request.get_json()

    # Extract data from request
    label = data['label']
    duration = data['duration']
    repetition = data['repetition']
    subject_shortcut = data['subject_shortcut']

    # Validate data (optional, but recommended)
    # For example, check if the subject exists, the duration is a positive number, etc.

    try:
        querry = Subject.query.filter_by(shortcut=subject_shortcut).first()
        if querry is None:
            return jsonify({'error': 'subject not found'}), 404

        new_teaching_activity = TeachingActivity(
            label=label,
            duration=duration,
            repetition=repetition,
            shortcut=subject_shortcut
        )
        # Add the new object to the database
        db.session.add(new_teaching_activity)
        db.session.commit()
        return jsonify(new_teaching_activity.as_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@my_routes.route('/deleteTeachingActivity/<string:label>', methods=['DELETE'])
def delete_teaching_activity(label):
    # Try to find the teaching activity by its ID
    teaching_activity = TeachingActivity.query.filter_by(label=label).first()

    if teaching_activity is None:
        # If the teaching activity doesn't exist, return a 404 error
        return jsonify({'error': 'Teaching activity not found'}), 404

    try:
        # If the teaching activity is found, delete it
        db.session.delete(teaching_activity)
        db.session.commit()
        return jsonify({'success': 'Teaching activity deleted'}), 200
    except Exception as e:
        # If there's an error during the deletion, rollback the session
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


