from flask import jsonify

def register_error_handlers(app):
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': "Bad Request"}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': "Unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': "Forbidden"}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': "Not found"}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': "Server Error"}), 500

    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({'error': "Service Unavailable"}), 503
