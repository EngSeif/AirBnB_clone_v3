#!/usr/bin/python3
""" Give The Status """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    obj = {
        "status": "OK"
    }
    return jsonify(obj)
