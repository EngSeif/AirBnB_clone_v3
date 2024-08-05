#!/usr/bin/python3
"""Handles all default RESTFul API actions for Amenity objects"""
from flask import abort, request, jsonify
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_place_review(place_id):
    """ retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all(Review).values()
    place_reviews = []
    for review in reviews:
        if review.place_id == place_id:
            place_reviews.append(review.to_dict())
    return jsonify(place_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """ Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_Review(place_id):
    """ Creates a Review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'text' not in data:
        abort(400, description="Missing text")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    data['place_id'] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    ignore_k = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_k:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
