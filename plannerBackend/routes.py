from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import Subject, User, db, Room
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


@my_routes.route('/deleteUser/<string:name>', methods=['DELETE'])
def delete_user(name):
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
            user.password = data['password']
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
    new_subject = Subject(
        shortcut=data['shortcut'],
        name=data['name'],
        annotation=data.get('annotation', ''),  # Optional field
        credits=data['credits'],
        id_guarantor=data['id_guarantor']
    )

    try:
        # Ensure the guarantor exists before adding the subject
        guarantor = User.query.get(data['id_guarantor'])
        if guarantor is None:
            return jsonify({'error': 'Guarantor user not found'}), 404

        db.session.add(new_subject)
        db.session.commit()
        return jsonify(new_subject.as_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@my_routes.route('/deleteSubject/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    try:
        subject = Subject.query.get(subject_id)
        if subject:
            db.session.delete(subject)
            db.session.commit()
            return '', 204  # No content
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


@my_routes.route('/createRoom', methods=['POST'])
def create_room():
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