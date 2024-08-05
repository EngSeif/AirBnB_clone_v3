#!/usr/bin/python3
""" App Main Page """
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def storagee_close(expection=None):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
