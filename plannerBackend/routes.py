from flask import Blueprint, request, jsonify
from plannerBackend.db import User, db
from sqlalchemy.orm.exc import NoResultFound

my_routes = Blueprint('my_routes', __name__)


@my_routes.route('/createUser', methods=['POST'])
def create_user():
    data = request.get_json()

    # Assuming your JSON data includes 'name', 'password', and 'role' fields
    new_user = User(name=data['name'], password=data['password'], role=data['role'])

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.as_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


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
