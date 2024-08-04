#!/usr/bin/python3
"""  handles all default RESTFul API actions """
from flask import abort, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def Get_all():
    """ Retrieves the list of all State """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return state_list


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def Get_state(state_id):
    """ Retrieves a State object """
    result = storage.get(State, state_id)
    if result is None:
        abort(404)
    else:
        return (result.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def Del_State(state_id):
    """ Deletes a State object """
    result = storage.get(State, state_id)
    if result is None:
        abort(404)
    else:
        cities = storage.all(City).values()
        for city in cities:
            if city.state_id == state_id:
                storage.delete(city)
        storage.delete(result)
        storage.save()
        return {}, 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def Create_State():
    """ Creates a State """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return (new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def Update_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    ignore_keys = ['id', 'created_at', 'updated_at']
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return (state.to_dict()), 200
