from flask import Flask
from config import settings
from routes.products import create_product_blueprint
from routes.orders import create_order_blueprint
from routes.payments import create_payment_blueprint
from routes.health import create_health_blueprint
from middleware.request_id_middleware import set_request_id, attach_id
from middleware.logger import entry_logger, exit_logger
from middleware.limitter import rate_limiter
from middleware.cors import  cors_settings
from middleware.errors_handler import register_error_handlers

def create_app(env_obj=None):
    app= Flask(__name__)
    
    if env_obj:
        app.config.from_object(env_obj)
    else:
        env = settings.FLASK_ENV or 'development'
        if env == 'production':
            app.config.from_object('config.settings.ProductionConfig')
        else:
            app.config.from_object('config.settings.DevelopmentConfig')


    register_error_handlers(app)
    app.before_request(set_request_id)
    app.after_request(attach_id)
    app.before_request(entry_logger)
    app.before_request(rate_limiter)
    app.after_request(exit_logger)
    app.register_blueprint(create_product_blueprint(), url_prefix='/products')
    app.register_blueprint(create_order_blueprint(), url_prefix='/orders')
    app.register_blueprint(create_health_blueprint(), url_prefix='/health')
    app.register_blueprint(create_payment_blueprint(), url_prefix='/payments')

    return app

if __name__ == '__main__':
    app = create_app()
    cors_settings(app)
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
