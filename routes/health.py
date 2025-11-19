from flask import Blueprint

def create_health_blueprint():
    health = Blueprint("health", __name__)

    @health.route('/', methods=['GET'])
    def get_health():
        return None
    return health
