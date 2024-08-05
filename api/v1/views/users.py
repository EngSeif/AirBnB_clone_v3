#!/usr/bin/python3
"""Handles all default RESTFul API actions for Amenity objects"""
from flask import abort, request, jsonify
from models import storage
from api.v1.views import app_views
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def Get_all_Users():
    """ Retrieves the list of all User objects """
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return users_list


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def Get_User(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return user.to_dict()


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def Del_User(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return {}, 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def Create_User():
    """ Creates a User """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return new_user.to_dict(), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def Update_User(user_id):
    """ Updates a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return user.to_dict(), 200
