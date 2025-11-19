#!/usr/bin/env python3

from dotenv import load_dotenv
import os

load_dotenv()

class BaseConfig:
    FLASK_ENV = os.getenv('FLASK_ENV')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes', 'on')
    LOG_LEVEL = os.getenv('LOG_LEVEL')
    HOST = os.getenv('HOST', 'localhost')
    PORT = int(os.getenv('PORT', 8000))
    TIMEZONE = os.getenv('TIMEZONE')
    RATE_LIMIT_REQUESTS_PER_MIN = int(os.getenv('RATE_LIMIT_REQUESTS_PER_MIN', 100))

class ProductionConfig(BaseConfig):
    DEBUG = False
    MONGO_URI = os.getenv('MONGO_PRO_URI')
    REDIS_HOST= os.getenv('REDIS_PRO_URI')
    KAFKA_BROKERS = os.getenv('KAFKA_PRO_URI')
    JWT_SECRET_KEY = os.getenv('PRODUCTION_KEY')
    RABBITMQ_HOST = os.getenv('RABBITMQ_PRO_URI')


class DevelopmentConfig(BaseConfig):
    MONGO_URI= os.getenv('MONGO_DEV_URI')
    DEBUG = True
    REDIS_HOST = os.getenv('REDIS_DEV_URI')
    KAFKA_BROKERS = os.getenv('KAFKA_DEV_URI')
    RABBITMQ_HOST = os.getenv('RABBITMQ_DEV_URI')
    JWT_SECRET_KEY = os.getenv('DEVELOPMENT_KEY')
