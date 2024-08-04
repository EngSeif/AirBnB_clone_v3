#!/usr/bin/python3
"""  handles all default RESTFul API actions """
from flask import abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all():
    """ Retrieves the list of all Amenity objects """
    ameniti = storage.all(Amenity).values()
    ameniti_list = [amen.to_dict() for amen in ameniti]
    return ameniti_list


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_ameniti(amenity_id):
    """ Retrieves a Amenity object """
    ameniti = storage.get(Amenity, amenity_id)
    if ameniti is None:
        abort(404)
    return ameniti.to_dict()


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_ameniti(amenity_id):
    """ Deletes a Amenity object """
    ameniti = storage.get(Amenity, amenity_id)
    if ameniti is None:
        abort(404)
    storage.delete(ameniti)
    storage.save()
    return {}, 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_ameniti():
    """ Creates a Amenity """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_ameniti = Amenity(**data)
    storage.new(new_ameniti)
    storage.save()
    return new_ameniti.to_dict()


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def Update_ameniti(amenity_id):
    """ Updates a Amenity object """
    ameniti = storage.get(Amenity, amenity_id)
    if ameniti is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(ameniti, key, value)
    storage.save()
    return ameniti.to_dict()
