from flask_cors import CORS

def cors_settings(app):
    CORS(app, resources = {
        r"/*": {
            "origins": ["http://localhost:8000"],
            "methods": ['GET', 'POST', 'DELETE', 'PUT'],
            "support_credentials": True,
            }
        })
