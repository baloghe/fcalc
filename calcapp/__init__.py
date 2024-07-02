import os

from flask import Flask

class ProductionConfig:
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')

class DevelopmentConfig:
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'secret-flask-calc'

def get_config_from_env():
    envname = os.getenv("FLASK_ENV", "development").lower()
    if envname == "production":
        return ProductionConfig()
    return DevelopmentConfig()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
        # SECRET_KEY=os.urandom(16) # 'dev'
    # )
    config = get_config_from_env()
    app.config.from_object(config)
    # config

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # calculator instance
    from .models import Calculator
    
    # views
    from .views import bp
    app.register_blueprint(bp)
    app.calc = Calculator()

    return app