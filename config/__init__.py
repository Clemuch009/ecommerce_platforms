from  config.settings import BaseConfig, ProductionConfig, DevelopmentConfig


if BaseConfig.FLASK_ENV == 'production':
    settings = DevelopmentConfig()
else:
    settings =  ProductionConfig()
